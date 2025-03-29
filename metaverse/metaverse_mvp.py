import asyncio
import json
import random
import sys
import os
import numpy as np
import pandas as pd
from datetime import datetime
from bson import ObjectId
from utils.logger import log_info, log_error
from ai_engine import DeepLearningPredictor
from database import fetch_metaverse_data, store_metaverse_activity
from utils.fake_data_provider import FakeDataProvider  # ✅ اتصال به داده‌های ساختگی پیشرفته

# اضافه کردن مسیر پروژه برای اطمینان از ایمپورت صحیح ماژول‌ها
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

INPUT_SHAPE = 10

# مقداردهی اولیه مدل یادگیری عمیق
dl_model = None
try:
    dl_model = DeepLearningPredictor(input_shape=INPUT_SHAPE)
except Exception as e:
    log_error(f"\ud83d\udea8 خطا در مقداردهی مدل یادگیری عمیق: {str(e)}")


async def connect_to_metaverse():
    """\ud83c\udf10 دریافت داده‌های زنده از سرورهای متاورس و ذخیره‌سازی (با fallback هوشمند)"""
    metaverse_data = FakeDataProvider.generate_metaverse_data()  # ⛓ دریافت داده واقع‌گرایانه

    record = {
        "_id": ObjectId(),
        "status": "Connected",
        "active_users": metaverse_data.get("users_online", 0),
        "server": random.choice(["AlphaZone", "BetaSim", "NeoGrid"]),
        "active_worlds": metaverse_data.get("active_worlds", []),
        "latest_event": metaverse_data.get("latest_event", {}),
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        await store_metaverse_activity(record)
        log_info(f"✅ اطلاعات متاورس ذخیره شد: {json.dumps({k: str(v) if k == '_id' else v for k, v in record.items()}, ensure_ascii=False)}")
    except Exception as e:
        log_error(f"❌ خطا در ذخیره‌سازی اطلاعات متاورس: {e}")

    return {
        "bot_name": "metaverse",
        "active_users": record["active_users"]
    }


async def run_metaverse_bot():
    """\ud83d\udd04 اجرای مداوم مانیتورینگ متاورس"""
    while True:
        await connect_to_metaverse()
        await asyncio.sleep(10)

def get_metaverse_activity():
    """📊 بازیابی داده‌های ساختگی متاورس برای استفاده در تست‌ها"""
    metaverse_data = FakeDataProvider.generate_metaverse_data()
    return {
        "users_online": metaverse_data.get("users_online", 0),
        "events_today": len(metaverse_data.get("active_worlds", []))  # یا تعداد دنیاهای فعال
    }


if __name__ == "__main__":
    log_info("✅ Metaverse Module Running...")
    try:
        asyncio.run(run_metaverse_bot())
    except RuntimeError as e:
        log_error(f"❌ خطا در اجرای متاورس: {e}")
