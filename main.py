import asyncio
import os
import sys
import time
import signal
import multiprocessing
import psutil
import redis
import requests
import uvicorn
from flask import Flask, jsonify

# 🧠 اضافه کردن مسیر پروژه برای دسترسی به ماژول‌ها
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# 📦 ماژول‌های داخلی پروژه
from utils.logger import log_info, log_error, log_warning
from blockchain.blockchain_mvp import fetch_transactions_from_network
from ai_teachers.ai_teacher_mvp import simulate_ai_teacher
from price_storage import store_price_data

# ⚙️ تلاش برای لود تنظیمات MVP
try:
    from config import MVP_CONFIG, ACTIVE_BOTS
except ImportError:
    log_error("❌ خطا: فایل `config.py` یافت نشد! اجرای برنامه متوقف شد.")
    exit(1)

# 🧩 تلاش برای لود ماژول‌های اصلی بات‌ها
try:
    from core import core_coordinator_mvp
    from security import cyber_defense_mvp
    from analytics import data_analysis_mvp
    from fintech import fintech_mvp
    from metaverse import metaverse_mvp
    from blockchain.blockchain_mvp import blockchain_mvp  # ✅ نمونه آماده از کلاس
except ImportError as e:
    log_error(f"❌ خطا در ایمپورت ماژول‌های اصلی: {e}")
    exit(1)

# 🛡 بررسی وجود ماژول blockchain_mvp (در صورتی که به صورت مستقل import شود)
try:
    from blockchain import blockchain_mvp
except ImportError:
    log_error("⚠️ هشدار: `blockchain_mvp` یافت نشد، این سرویس غیرفعال خواهد بود.")
    blockchain_mvp = None

# 🔌 اتصال به Redis
try:
    redis_client = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
    redis_client.ping()
except redis.ConnectionError:
    log_error("❌ خطا: Redis در دسترس نیست، پیام‌رسانی بین بات‌ها غیرفعال خواهد بود.")
    redis_client = None
    
    url = f"http://{os.getenv('API_HOST', 'localhost')}:8000/api/active_bots"

# 🚀 مقداردهی اولیه Flask
app = Flask(__name__)
bot_status = {}

@app.route("/")
def index():
    return """
    <h1>👋 خوش آمدید به Nexus-AITech MVP</h1>
    <p>برای مشاهده وضعیت سیستم، به <a href='/api/status'>/api/status</a> مراجعه کنید.</p>
    <p>برای دریافت لیست بات‌های فعال، به <a href='/api/active_bots'>/api/active_bots</a> بروید.</p>
    """

@app.route("/api/status", methods=["GET"])
def get_system_status():
    return jsonify({
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "active_bots": dict(bot_status) if bot_status else {}
    })

@app.route("/api/active_bots", methods=["GET"])
def get_active_bots():
    return jsonify({"active_bots": list(bot_status.keys())})

async def run_fintech_bot():
    await fintech_mvp.process_transaction({
        "transaction_id": "demo_tx",
        "amount": 100,
        "user": "test"
    })

BOTS = {
    "cyber_defense": cyber_defense_mvp.detect_threats,
    "data_analysis": data_analysis_mvp.analyze_data,
    "fintech": run_fintech_bot,  # 👈 اصلاح‌شده
    "ai_teacher": simulate_ai_teacher,
    "metaverse": metaverse_mvp.connect_to_metaverse,
    "blockchain": blockchain_mvp.check_blockchain_status
}

def run_api():
    port = int(os.getenv("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

def wait_for_api_ready():
    for _ in range(10):
        try:
            r = requests.get("http://localhost:8000/api/status")
            if r.status_code == 200:
                print("✅ API آماده است.")
                return
        except Exception:
            print("⏳ در حال انتظار برای API...")
        time.sleep(1)

async def async_run_bot(bot_name, bot_status):
    while True:
        try:
            if bot_name in BOTS:
                log_info(f"🔵 در حال اجرای بات: {bot_name} ...")
                bot_status[bot_name] = "Running"

                if redis_client:
                    redis_client.publish("bot_status", f"{bot_name}: Running")

                bot_function = BOTS[bot_name]

                if asyncio.iscoroutinefunction(bot_function):
                    await bot_function()
                else:
                    bot_function()

                await asyncio.sleep(5)
            else:
                log_warning(f"⚠️ بات `{bot_name}` در لیست موجود نیست!")
                bot_status[bot_name] = "Not Found"
                break

        except Exception as e:
            log_error(f"❌ خطا در بات `{bot_name}`: {e}")
            bot_status[bot_name] = "Crashed"
            if redis_client:
                redis_client.publish("bot_status", f"{bot_name}: Crashed")
            log_info(f"🔄 تلاش مجدد برای راه‌اندازی `{bot_name}` در ۵ ثانیه ...")
            await asyncio.sleep(5)

def initialize_manager(manager):
    shared_status = manager.dict()
    for bot in ACTIVE_BOTS:
        shared_status[bot] = "Initializing"
    return shared_status

def run_bot(bot_name, bot_status):
    asyncio.run(async_run_bot(bot_name, bot_status))

def start_mvp(manager):
    global bot_status
    bot_status = initialize_manager(manager)
    log_info("🚀 در حال راه‌اندازی MVP...")

    api_process = multiprocessing.Process(target=run_api)
    api_process.start()

    processes = []
    for bot_name in ACTIVE_BOTS:
        p = multiprocessing.Process(target=run_bot, args=(bot_name, bot_status))
        p.start()
        processes.append(p)
        time.sleep(1)

    log_info("✅ همه بات‌ها در حال اجرا هستند.")

    def graceful_shutdown(signum, frame):
        log_info("🛑 سیگنال خاموش شدن دریافت شد. توقف بات‌ها و API...")
        for p in processes:
            p.terminate()
        api_process.terminate()
        log_info("✅ همه پردازش‌ها متوقف شدند.")
        exit(0)

    signal.signal(signal.SIGINT, graceful_shutdown)
    signal.signal(signal.SIGTERM, graceful_shutdown)

    for p in processes:
        p.join()

@app.route("/")
def home():
    return {"message": "✅ Nexus-AITech MVP is running!", "status": "Active Bots"}

if __name__ == "__main__":
    multiprocessing.freeze_support()
    manager = multiprocessing.Manager()
    start_mvp(manager)
    log_info("✅ `main.py` با موفقیت اجرا شد.")
