import asyncio
import json
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from utils.logger import log_info, log_error
from ai_engine import CryptoPredictor
from market_api import get_live_crypto_price
from price_storage import store_price_data

# اضافه کردن مسیر پروژه برای اطمینان از ایمپورت صحیح ماژول‌ها
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

# مدل یادگیری عمیق برای پیش‌بینی قیمت ارز دیجیتال
crypto_model = CryptoPredictor()

async def fetch_real_market_data():
    """📊 دریافت قیمت زنده از بازار ارز دیجیتال"""
    try:
        live_price = await get_live_crypto_price("NXAIT")
        timestamp = datetime.now()
        await store_price_data(live_price, timestamp)
        log_info(f"📊 قیمت زنده NXAIT: {live_price} در زمان {timestamp}")
        return live_price
    except Exception as e:
        log_error(f"❌ خطا در دریافت قیمت زنده: {e}")
        return None

async def predict_future_price():
    """📈 پیش‌بینی قیمت آینده NXAIT با مدل هوش مصنوعی"""
    try:
        predicted_price = await crypto_model.predict_price()
        log_info(f"📈 پیش‌بینی قیمت آینده NXAIT: {predicted_price}")
        return predicted_price
    except Exception as e:
        log_error(f"❌ خطا در پیش‌بینی قیمت: {e}")
        return None

async def visualize_market_data():
    """📊 نمایش نمودار قیمت زنده و پیش‌بینی آینده"""
    try:
        live_price = await fetch_real_market_data()
        predicted_price = await predict_future_price()
        
        if live_price is None or predicted_price is None:
            log_error("⚠️ داده‌های قیمت کامل نیستند. نمودار نمایش داده نمی‌شود.")
            return
        
        plt.figure(figsize=(10, 5))
        plt.bar(["Live Price", "Predicted Price"], [live_price, predicted_price], color=["blue", "green"])
        plt.title("📊 قیمت زنده و پیش‌بینی قیمت NXAIT")
        plt.ylabel("قیمت (NXAIT)")
        plt.grid(True)
        plt.show()
    except Exception as e:
        log_error(f"❌ خطا در نمایش نمودار: {e}")

async def run_financial_simulation():
    """ اجرای مداوم شبیه‌سازی مالی """
    while True:
        await visualize_market_data()
        await asyncio.sleep(10)  # به‌روزرسانی قیمت زنده هر 10 ثانیه

if __name__ == "__main__":
    log_info("🚀 Financial Simulation در حال راه‌اندازی...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_financial_simulation())