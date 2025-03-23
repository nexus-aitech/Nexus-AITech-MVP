import asyncio
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
import threading
import requests
from flask import Flask, request, jsonify
from config import MVP_CONFIG
from utils.logger import log_info, log_error
from integrations.realtime_api_connectors import (
    get_kucoin_price,
    get_coinmarketcap_price,
    get_bingx_price,
    get_bitget_price,
    get_latest_blockchain_data
)

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

app = Flask(__name__)

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
    return jsonify({"status": "Core Coordinator is Running!", "message": "Use /api/process or /status to interact."})

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
        log_error(f"🚨 خطا در process_request: {str(e)}")
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
    while True:
        try:
            kucoin_data = await get_kucoin_price()
            cmc_data = await get_coinmarketcap_price()
            bingx_data = await get_bingx_price()
            bitget_data = await get_bitget_price()
            blockchain_data = await get_latest_blockchain_data()

            bot_status["fintech"] = {
                "status": "Running",
                "kucoin_price": kucoin_data,
                "coinmarketcap_price": cmc_data,
                "bingx_price": bingx_data,
                "bitget_price": bitget_data
            }
            bot_status["blockchain"] = {
                "status": "Running",
                "latest_block": blockchain_data.get("latest_block_hex")
            }

        except Exception as e:
            log_error(f"🚨 خطا در اجرای بات‌ها: {str(e)}")

        await asyncio.sleep(10)

def start_async_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(update_bots())

threading.Thread(target=start_async_loop, daemon=True).start()

if __name__ == "__main__":
    log_info("🔥 راه‌اندازی Core Coordinator...")
    app.run(
        host=MVP_CONFIG.get("HOST", "0.0.0.0"),
        port=5002,
        debug=MVP_CONFIG.get("DEBUG", False),
        threaded=True
    )
