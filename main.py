import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import multiprocessing
from blockchain.blockchain_mvp import fetch_transactions_from_network
import threading
import time
import signal
import psutil
import redis
import asyncio
from flask import Flask, jsonify
from utils.logger import log_info, log_error, log_warning
from ai_teachers.ai_teacher_mvp import simulate_ai_teacher
from price_storage import store_price_data

# مقداردهی اولیه
def initialize_manager(manager):
    """مقداردهی `bot_status` با `multiprocessing.Manager` از پردازش اصلی"""
    bot_status = manager.dict()
    for bot in ACTIVE_BOTS:
        bot_status[bot] = "Initializing"
    return bot_status

# تلاش برای ایمپورت تنظیمات
try:
    from config import MVP_CONFIG, ACTIVE_BOTS
except ImportError:
    log_error("❌ خطا: `config.py` یافت نشد! اجرای برنامه متوقف شد.")
    exit(1)

# تلاش برای ایمپورت ماژول‌های مرتبط با بات‌ها
try:
    from core import core_coordinator_mvp
    from security import cyber_defense_mvp
    from analytics import data_analysis_mvp
    from fintech import fintech_mvp
    from metaverse import metaverse_mvp
    from ai_teachers.ai_teacher_mvp import simulate_ai_teacher
    from blockchain.blockchain_mvp import check_blockchain_status
except ImportError as e:
    log_error(f"❌ خطا در ایمپورت ماژول‌های اصلی: {e}")
    exit(1)

# بررسی و مدیریت `blockchain_mvp`
try:
    from blockchain import blockchain_mvp
except ImportError:
    log_error("⚠️ هشدار: `blockchain_mvp` یافت نشد، این سرویس غیرفعال خواهد بود.")
    blockchain_mvp = None

# تنظیم `Redis` برای مدیریت پیام‌ها بین بات‌ها
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_client.ping()
except redis.ConnectionError:
    log_error("❌ خطا: `Redis` در دسترس نیست، پیام‌رسانی بین بات‌ها غیرفعال خواهد بود.")
    redis_client = None

# تنظیم Flask API برای مانیتورینگ سلامت MVP
app = Flask(__name__)

@app.route("/api/status", methods=["GET"])
def get_system_status():
    """📡 API بررسی وضعیت منابع سیستم و سلامت MVP"""
    return jsonify({
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "active_bots": dict(bot_status) if bot_status else {}
    })

# تعریف سرویس‌های اصلی
BOTS = {
    "cyber_defense": cyber_defense_mvp.detect_threats,
    "data_analysis": data_analysis_mvp.analyze_data,
    "fintech": lambda: asyncio.run(fintech_mvp.process_transaction()),
    "ai_teacher": lambda: asyncio.run(simulate_ai_teacher()),
    "metaverse": lambda: asyncio.run(metaverse_mvp.connect_to_metaverse()),
    "blockchain": blockchain_mvp.check_blockchain_status if blockchain_mvp else lambda: log_error("⚠️ `blockchain_mvp` غیرفعال است."),
}

def run_api():
    """اجرای Flask API مانیتورینگ"""
    PORT = int(os.getenv("PORT", 5002))  # دریافت پورت از ENV یا استفاده از پیش‌فرض
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)

def async_run_bot(bot_name, bot_status):
    """اجرای بات‌های async با مقداردهی صحیح `bot_status`"""
    while True:
        try:
            if bot_name in BOTS:
                log_info(f"🔵 در حال اجرای بات: {bot_name} ...")
                bot_status[bot_name] = "Running"
                if redis_client:
                    redis_client.publish("bot_status", f"{bot_name}: Running")

                bot_function = BOTS[bot_name]
                if asyncio.iscoroutinefunction(bot_function):
                    asyncio.run(bot_function())  # اجرای توابع async
                else:
                    bot_function()  # اجرای توابع معمولی

                time.sleep(5)  # تاخیر برای جلوگیری از اجرای بی‌وقفه
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
            time.sleep(5)

def run_bot(bot_name, bot_status):
    """اجرای بات‌های معمولی در پردازش جداگانه"""
    asyncio.run(async_run_bot(bot_name, bot_status))

def start_mvp(manager):
    """🔥 اجرای تمام بات‌های فعال با `multiprocessing`"""
    global bot_status
    bot_status = initialize_manager(manager)  # مقداردهی `bot_status` از پردازش اصلی

    log_info("🚀 MVP در حال راه‌اندازی است...")

    # اجرای API در پردازش جداگانه
    api_process = multiprocessing.Process(target=run_api)
    api_process.start()

    # اجرای سایر بات‌ها در پردازش‌های جداگانه
    processes = []
    for bot_name in ACTIVE_BOTS:
        p = multiprocessing.Process(target=run_bot, args=(bot_name, bot_status))
        processes.append(p)
        p.start()
        time.sleep(1)  # تأخیر کوتاه برای جلوگیری از تداخل

    log_info("✅ تمامی بات‌ها در حال اجرا هستند.")

    def graceful_shutdown(signum, frame):
        log_info("🔴 دریافت سیگنال خاموش شدن، توقف پردازش‌ها...")
        for p in processes:
            p.terminate()
        api_process.terminate()
        log_info("✅ تمامی پردازش‌ها متوقف شدند.")
        exit(0)

    signal.signal(signal.SIGINT, graceful_shutdown)
    signal.signal(signal.SIGTERM, graceful_shutdown)

    # نگه داشتن پردازش‌های بات‌ها
    for p in processes:
        p.join()

if __name__ == "__main__":
    multiprocessing.freeze_support()  # مخصوص ویندوز برای جلوگیری از crash
    
    # مقداردهی `multiprocessing.Manager` فقط در پردازش اصلی
    manager = multiprocessing.Manager()
    
    # اجرای `start_mvp`
    start_mvp(manager)

    # نمایش لاگ شروع برنامه
    log_info("✅ `main.py` با موفقیت اجرا شد.")
