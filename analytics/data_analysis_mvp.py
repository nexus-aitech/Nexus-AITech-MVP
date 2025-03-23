import asyncio
import logging
import sys
import os
import random
import json
import requests
import pandas as pd
from datetime import datetime
from utils.logger import log_info, log_error
from ai_engine import DataAnalyzer
from database import fetch_real_data, store_analysis_result

# اضافه کردن مسیر پروژه برای اطمینان از ایمپورت صحیح ماژول‌ها
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

# تنظیمات لاگ‌گیری
logger = logging.getLogger("DataAnalysis")

# مدل هوش مصنوعی برای تحلیل داده‌ها
data_analyzer = DataAnalyzer()

# آدرس سرور مرکزی (در صورت نیاز)
CORE_URL = os.getenv("CORE_URL", "http://localhost:5000/api/process")

def simulate_data_analysis(num_samples=10):
    """ شبیه‌سازی تحلیل داده‌ها برای تست سیستم """
    try:
        data = {
            "feature_1": [random.uniform(0, 1) for _ in range(num_samples)],
            "feature_2": [random.randint(1, 100) for _ in range(num_samples)],
            "feature_3": [random.choice(["A", "B", "C"]) for _ in range(num_samples)],
            "timestamp": [datetime.utcnow() for _ in range(num_samples)]
        }
        
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        log_error(f"❌ خطا در شبیه‌سازی تحلیل داده‌ها: {e}")
        return pd.DataFrame()

async def analyze_data():
    """📊 تحلیل داده‌های واقعی و پردازش پیشرفته"""
    log_info("📊 در حال دریافت و پردازش داده‌های واقعی...")
    try:
        real_data = await fetch_real_data()
        analyzed_result = await data_analyzer.analyze(real_data)
        await store_analysis_result(analyzed_result, datetime.now())
    
        log_info(f"📊 نتایج تحلیل: {json.dumps(analyzed_result, ensure_ascii=False)}")
    
        try:
            response = requests.post(CORE_URL, json={"bot_name": "data_analysis", "processed_data": analyzed_result}, timeout=5)
            if response.status_code == 200:
                data = response.json()
                log_info(f"✅ گزارش تحلیل از سرور مرکزی دریافت شد: {data.get('response', 'No response data')}")
            else:
                log_error(f"❌ خطا در دریافت گزارش از Core Coordinator! وضعیت: {response.status_code}")
        except requests.exceptions.ConnectionError:
            log_error("🚨 Core Coordinator در دسترس نیست! تحلیل مستقل انجام می‌شود...")
        except requests.exceptions.Timeout:
            log_error("⏳ درخواست به Core Coordinator تایم‌اوت شد. تحلیل محلی ادامه دارد.")
    except Exception as e:
        log_error(f"⚠️ خطای غیرمنتظره: {e}")

async def run_continuous_analysis():
    while True:
        await analyze_data()
        await asyncio.sleep(10)

# فقط اگر مستقیم اجرا شود
if __name__ == "__main__":
    log_info("🚀 Data Analysis Module در حال راه‌اندازی...")
    try:
        asyncio.run(run_continuous_analysis())
    except RuntimeError as e:
        log_error(f"❌ خطا در اجرای Data Analysis: {e}")