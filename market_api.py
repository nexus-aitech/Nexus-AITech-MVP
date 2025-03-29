import asyncio
import os
import requests
from dotenv import load_dotenv
from config import EXCHANGE_APIS

# بارگذاری متغیرهای محیطی
load_dotenv()

# دریافت API Key از .env یا EXCHANGE_APIS
COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY") or EXCHANGE_APIS.get("coinmarketcap")

def get_live_crypto_price(symbol="BTC"):
    """
    دریافت قیمت زنده از CoinMarketCap با API Key
    """
    if not COINMARKETCAP_API_KEY:
        print("❌ خطا: کلید API برای CoinMarketCap مقداردهی نشده است.")
        return 0

    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    parameters = {
        "symbol": symbol.upper(),
        "convert": "USD"
    }
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY
    }

    try:
        response = requests.get(url, headers=headers, params=parameters, timeout=5)
        response.raise_for_status()  # اگر خطایی در درخواست باشد، این خط اجرا می‌شود
        data = response.json()
        return round(data["data"][symbol.upper()]["quote"]["USD"]["price"], 2)
    except requests.exceptions.RequestException as e:
        print(f"❌ خطای اتصال به API: {e}")
        return 0
