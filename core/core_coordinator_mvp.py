import asyncio
import sys
import os
import json
import traceback
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from threading import Thread

# لود متغیرهای محیطی
load_dotenv()

# تنظیم asyncio برای ویندوز
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# 🛠 افزودن مسیر `integrations` به `sys.path`
BASE_DIR = os.path.abspath(os.path.dirname(__file__) + "/..")
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "integrations"))

# ایمپورت ماژول‌های مورد نیاز
from config import MVP_CONFIG
from utils.logger import log_info, log_error
from integrations.realtime_api_connectors import (
    get_kucoin_price,
    get_coinmarketcap_price,
    get_bingx_price,
    get_bitget_price,
    get_latest_blockchain_data
)

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))

# وضعیت بات‌ها
bot_status = {
    "ai_teacher": {"status": "Initializing", "students_online": 0, "lesson": None},
    "blockchain": {"status": "Initializing", "latest_block": 0, "transactions": 0},
    "metaverse": {"status": "Initializing", "active_users": 0},
    "fintech": {"status": "Initializing", "transactions": 0},
    "data_analysis": {"status": "Initializing", "processed_data": {}},
    "cyber_defense": {"status": "Initializing", "threats_detected": 0}
}

@app.route("/", methods=["GET"])
def home():
    """ بررسی `index.html`، در غیر این صورت پیام JSON برمی‌گرداند. """
    template_path = os.path.join(BASE_DIR, "templates", "index.html")
    
    if not os.path.exists(template_path):
        return jsonify({
            "message": "✅ Nexus-AITech MVP is running!",
            "status": "Active Bots",
            "API": "/api/status"
        }), 200
    
    return render_template("index.html")

@app.route("/api/process", methods=["POST"])
def process_request():
    try:
        data = request.get_json()
        if not data:
            log_error("❌ درخواست بدون JSON دریافت شد!")
            return jsonify({"error": "Invalid JSON payload"}), 400

        bot_name = data.get("bot_name")
        if bot_name not in bot_status:
            log_error(f"❌ درخواست نامعتبر: {bot_name} در لیست بات‌ها نیست.")
            return jsonify({"error": "Invalid bot name"}), 400

        bot_status[bot_name]["status"] = "Running"
        bot_status[bot_name].update(data)

        log_info(f"✅ وضعیت {bot_name} بروزرسانی شد: {data}")
        return jsonify({"bot": bot_name, "status": bot_status[bot_name]})

    except Exception as e:
        log_error(f"🚨 خطا در process_request: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/status", methods=["GET"])
def get_status():
    return jsonify({"status": bot_status, "message": "MVP is running"})

@app.route("/api/active_bots", methods=["GET"])
def get_active_bots():
    active = {
        name: data for name, data in bot_status.items()
        if data.get("status") == "Running"
    }
    return jsonify({"active_bots": active, "total": len(active)})

async def update_bots():
    """ بروزرسانی اطلاعات بات‌ها از APIها با مدیریت خطا و تلاش مجدد """
    while True:
        try:
            # تعریف دیکشنری برای درخواست‌ها
            tasks = {
                "kucoin": get_kucoin_price(),
                "coinmarketcap": get_coinmarketcap_price(),
                "bingx": get_bingx_price(),
                "bitget": get_bitget_price(),
                "blockchain": get_latest_blockchain_data()
            }

            results = await asyncio.gather(*tasks.values(), return_exceptions=True)

            # بررسی و ذخیره نتایج API
            for key, result in zip(tasks.keys(), results):
                if isinstance(result, Exception):
                    log_error(f"🚨 خطا در دریافت {key}: {result}")
                else:
                    bot_status["fintech"][f"{key}_price"] = result.get("price") if result else None
            
            bot_status["blockchain"]["latest_block"] = results[-1].get("latest_block_hex") if results[-1] else None
            log_info("✅ وضعیت بات‌های فین‌تک و بلاکچین بروزرسانی شد.")

        except Exception as e:
            log_error(f"🚨 خطا در اجرای بات‌ها: {str(e)}\n{traceback.format_exc()}")

        await asyncio.sleep(10)

async def main():
    """ اجرای همزمان `Flask` و `update_bots()` """
    log_info("🚀 راه‌اندازی هماهنگ Flask و بات‌ها")

    loop = asyncio.get_event_loop()

    # بررسی بسته نبودن لوپ قبل از اجرای `asyncio.run()`
    if loop.is_closed():
        log_error("❌ حلقه asyncio بسته است! اجرای مجدد ممکن نیست.")
        return

    # راه‌اندازی `update_bots()`
    loop.create_task(update_bots())

    def run_flask():
        port = int(os.getenv("PORT", 8050))
        app.run(host="0.0.0.0", port=port, debug=MVP_CONFIG.get("DEBUG", False), use_reloader=False)

    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
