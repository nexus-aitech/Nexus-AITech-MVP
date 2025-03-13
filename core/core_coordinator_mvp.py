import json
import random
import logging
from flask import Flask, request, jsonify
from functools import lru_cache

# تنظیمات لاگ‌گیری برای Debugging بهتر
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ایجاد اپلیکیشن Flask برای مدیریت درخواست‌ها
app = Flask(__name__)

# داده‌های تستی برای پاسخ به سایر بات‌ها
mock_responses = {
    "cyber_defense": {"status": "Active", "threats_detected": 2},
    "data_analysis": {"summary": "Basic data insights generated."},
    "fintech": {"transaction_status": "Success", "amount": "100 NXAIT"},
    "metaverse": {"connection": "Established", "active_users": 125},
    "ai_teacher": {"lesson": "Introduction to AI", "students_online": 30},
    "blockchain": {"network_status": "Connected", "latest_block": 1457892},
}

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Core Coordinator is Running!", "message": "Use /api/process to interact."})


# استفاده از کش برای جلوگیری از پردازش‌های تکراری

def get_mock_response(bot_name):
    if bot_name == "cyber_defense":
        return {"status": "Active", "threats_detected": random.randint(0, 10)}
    elif bot_name == "data_analysis":
        return {"summary": f"Analysis {random.randint(1, 100)} completed"}
    elif bot_name == "fintech":
        return {
            "transaction_status": "Success" if random.choice([True, False]) else "Failed",
            "amount": f"{random.randint(10, 500)} NXAIT"
        }
    elif bot_name == "metaverse":
        return {"connection": "Established", "active_users": random.randint(50, 500)}
    elif bot_name == "blockchain":
        return {"network_status": "Connected", "latest_block": random.randint(1000000, 2000000)}
    return {}

@app.route("/api/process", methods=["POST"])
def process_request():
    try:
        data = request.get_json()
        if not data:
            logging.error("❌ درخواست بدون JSON دریافت شد!")
            return jsonify({"error": "Invalid JSON payload"}), 400

        bot_name = data.get("bot_name")
        if not bot_name:
            logging.warning("⚠️ درخواست نامعتبر: bot_name ارسال نشده است.")
            return jsonify({"error": "Missing bot_name parameter"}), 400

        response = get_mock_response(bot_name)
        if response:
            logging.info(f"✅ پردازش موفقیت‌آمیز برای بات: {bot_name}")
            return jsonify({"bot": bot_name, "response": response})
        else:
            logging.warning(f"❌ درخواست نامعتبر: {bot_name} یافت نشد!")
            return jsonify({"error": "Invalid bot request"}), 400

    except Exception as e:
        logging.error(f"🚨 خطا در پردازش درخواست: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

        # بررسی صحت درخواست
        if not bot_name:
            logging.warning("Received invalid request: Missing bot_name")
            return jsonify({"error": "Missing bot_name parameter"}), 400

        # دریافت داده از کش یا پاسخ‌های تستی
        response = get_mock_response(bot_name)

        if response:
            logging.info(f"Processed request for bot: {bot_name}")
            return jsonify({"bot": bot_name, "response": response})
        else:
            logging.warning(f"Invalid bot request received: {bot_name}")
            return jsonify({"error": "Invalid bot request"}), 400

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500


if __name__ == "__main__":
    logging.info("Starting AI Core Coordinator MVP...")
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)

# Core Coordinator MVP Initialized
print('✅ Core Coordinator MVP is Running!')
