import asyncio
import json
import random
import sys
import os
import numpy as np
import pandas as pd
from datetime import datetime
from utils.logger import log_info, log_error
from ai_engine import DeepLearningPredictor
from database import fetch_metaverse_data, store_metaverse_activity

# اضافه کردن مسیر پروژه برای اطمینان از ایمپورت صحیح ماژول‌ها
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

INPUT_SHAPE = 10

# مقداردهی اولیه مدل یادگیری عمیق
try:
    dl_model = DeepLearningPredictor(input_shape=INPUT_SHAPE)
except Exception as e:
    log_error(f"🚨 خطا در مقداردهی مدل یادگیری عمیق: {str(e)}")
    dl_model = None

async def connect_to_metaverse():
    """🌐 دریافت داده‌های زنده از سرورهای متاورس و ذخیره‌سازی"""
    try:
        live_data = await fetch_metaverse_data()
        if not live_data:
            log_info("⚠️ داده‌ای از متاورس دریافت نشد. مقدار پیش‌فرض استفاده می‌شود.")
            live_data = {"active_users": 0, "server": "Unknown"}

        active_users = live_data.get("active_users", 0)
        server_name = live_data.get("server", "Unknown")
        
        metaverse_data = {
            "status": "Connected",
            "active_users": active_users,
            "server": server_name,
            "timestamp": datetime.now().isoformat()
        }

        try:
            await store_metaverse_activity(metaverse_data)
            log_info(f"🌐 اطلاعات زنده متاورس: {json.dumps(metaverse_data, ensure_ascii=False)}")
        except Exception as e:
            log_error(f"🚨 خطا در ذخیره‌سازی داده‌های متاورس: {str(e)}")
        
        return {
            "bot_name": "metaverse",
            "active_users": active_users
        }
    
    except Exception as e:
        log_error(f"🚨 خطا در دریافت داده‌های متاورس: {str(e)}")
        return {"bot_name": "metaverse", "active_users": 0}

async def run_metaverse_bot():
    """🔄 اجرای مداوم مانیتورینگ متاورس"""
    while True:
        await connect_to_metaverse()
        await asyncio.sleep(10)

# فقط اگر مستقیم اجرا شود
if __name__ == "__main__":
    log_info("✅ Metaverse Module Running...")
    try:
        asyncio.run(run_metaverse_bot())
    except RuntimeError as e:
        log_error(f"❌ خطا در اجرای متاورس: {e}")
