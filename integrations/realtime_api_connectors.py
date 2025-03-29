import asyncio
import aiohttp
import os
import json
from dotenv import load_dotenv

# لود متغیرهای محیطی
load_dotenv()

# تنظیم زمان پیش‌فرض برای درخواست‌ها
TIMEOUT = aiohttp.ClientTimeout(total=10)
RETRY_ATTEMPTS = 3  # تعداد دفعات تلاش مجدد برای درخواست‌ها

# دریافت API Key ها از .env
API_KEYS = {
    "KUCOIN": os.getenv("KUCOIN_API_KEY"),
    "BINGX": os.getenv("BINGX_API_KEY"),
    "BITGET": os.getenv("BITGET_API_KEY"),
    "COINMARKETCAP": os.getenv("COINMARKETCAP_API_KEY"),
    "ANKR": os.getenv("ANKR_API_KEY"),
}

# دریافت آدرس‌های API از .env
BLOCKCHAIN_APIS = {
    "ANKR": os.getenv("ANKR_API_KEY"),
    "ALCHEMY_ETH": os.getenv("ALCHEMY_ETH_MAINNET"),
    "ALCHEMY_AVAX": os.getenv("ALCHEMY_AVAX_MAINNET"),
    "INFURA_ARB": os.getenv("INFURA_ARB_MAINNET"),
}

async def fetch_with_retry(session, method, url, headers=None, params=None, json_data=None, retries=RETRY_ATTEMPTS):
    """ ارسال درخواست با قابلیت تلاش مجدد در صورت خطاهای موقت """
    for attempt in range(retries):
        try:
            async with session.request(method, url, headers=headers, params=params, json=json_data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"⚠️ درخواست به {url} با خطا {response.status} مواجه شد. تلاش {attempt + 1}...")
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"⚠️ خطای شبکه در {url}: {e}. تلاش {attempt + 1}...")
        await asyncio.sleep(1)  # کمی تأخیر قبل از تلاش مجدد
    return None

# ==== دریافت قیمت از KuCoin ====
async def get_kucoin_price(symbol="ETH-USDC"):
    url = f"https://api.kucoin.com/api/v1/market/stats?symbol={symbol}"
    headers = {"KC-API-KEY": API_KEYS["KUCOIN"]}
    
    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        data = await fetch_with_retry(session, "GET", url, headers=headers)
        return {"symbol": symbol, "price": data.get("data", {}).get("last") if data else None}

# ==== دریافت آخرین بلاک ====
async def get_latest_blockchain_data():
    url = BLOCKCHAIN_APIS["ANKR"]
    headers = {"Content-Type": "application/json"}
    payload = {"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1}

    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        data = await fetch_with_retry(session, "POST", url, headers=headers, json_data=payload)
        return {"latest_block_hex": data.get("result") if data else None}

# ==== دریافت قیمت از CoinMarketCap ====
async def get_coinmarketcap_price(symbol="SOL"):
    url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={symbol}"
    headers = {"X-CMC_PRO_API_KEY": API_KEYS["COINMARKETCAP"]}

    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        data = await fetch_with_retry(session, "GET", url, headers=headers)
        return {
            "symbol": symbol,
            "price": data.get("data", {}).get(symbol, {}).get("quote", {}).get("USD", {}).get("price") if data else None
        }

# ==== دریافت قیمت از BingX ====
async def get_bingx_price(symbol="ARB-USDC"):
    url = f"https://open-api.bingx.com/openApi/swap/v2/quote/price?symbol={symbol}"
    headers = {"X-BX-APIKEY": API_KEYS["BINGX"]}

    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        data = await fetch_with_retry(session, "GET", url, headers=headers)
        return {"symbol": symbol, "price": data.get("price") if data else None}

# ==== دریافت قیمت از Bitget ====
async def get_bitget_price(symbol="AVAX_USDC"):
    url = f"https://api.bitget.com/api/spot/v1/market/ticker?symbol={symbol}"
    headers = {"ACCESS-KEY": API_KEYS["BITGET"]}

    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        data = await fetch_with_retry(session, "GET", url, headers=headers)
        return {
            "symbol": symbol,
            "price": data.get("data", {}).get("last") if data else None
        }

# ==== تست عملکرد APIها ====
async def test_apis():
    results = await asyncio.gather(
        get_kucoin_price(),
        get_latest_blockchain_data(),
        get_coinmarketcap_price(),
        get_bingx_price(),
        get_bitget_price()
    )
    print(json.dumps(results, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(test_apis())
