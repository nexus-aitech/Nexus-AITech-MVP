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

# اطمینان از مسیر درست پروژه برای import
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY")

# مدل پیش‌بینی قیمت ارز دیجیتال
crypto_model = CryptoPredictor()

async def fetch_real_market_data():
    """📊 دریافت قیمت زنده از بازار"""
    try:
        price = await get_live_crypto_price("NXAIT")
        timestamp = datetime.utcnow().isoformat()
        await store_price_data("NXAIT", price, timestamp)
        log_info(f"📊 قیمت زنده NXAIT: {price} در {timestamp}")
        return price
    except Exception as e:
        log_error(f"❌ خطا در دریافت قیمت زنده: {e}")
        return None

async def predict_future_price():
    """📈 پیش‌بینی قیمت آینده با مدل هوش مصنوعی"""
    try:
        predicted_price = await crypto_model.predict_price()
        log_info(f"📈 پیش‌بینی قیمت آینده NXAIT: {predicted_price}")
        return predicted_price
    except Exception as e:
        log_error(f"❌ خطا در پیش‌بینی قیمت: {e}")
        return None

async def visualize_market_data():
    """📉 رسم نمودار قیمت زنده و پیش‌بینی"""
    try:
        live_price = await fetch_real_market_data()
        predicted_price = await predict_future_price()

        if live_price is None or predicted_price is None:
            log_warning("⚠️ داده‌های قیمت کامل نیستند. نمودار رسم نمی‌شود.")
            return

        plt.figure(figsize=(10, 5))
        plt.bar(["Live Price", "Predicted Price"], [live_price, predicted_price], color=["blue", "green"])
        plt.title("📊 قیمت زنده و پیش‌بینی شده NXAIT")
        plt.ylabel("قیمت (USDC)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("market_simulation.png")  # ذخیره نمودار به‌جای نمایش GUI
        log_info("📊 نمودار قیمت ذخیره شد: market_simulation.png")
    except Exception as e:
        log_error(f"❌ خطا در رسم نمودار: {e}")

async def run_financial_simulation():
    """🔄 اجرای حلقه شبیه‌سازی مالی"""
    while True:
        await visualize_market_data()
        await asyncio.sleep(10)  # اجرا در هر ۱۰ ثانیه

if __name__ == "__main__":
    log_info("🚀 شبیه‌سازی مالی NXAIT در حال اجراست...")
    try:
        asyncio.run(run_financial_simulation())
    except Exception as e:
        log_error(f"❌ خطا در اجرای شبیه‌سازی: {e}")