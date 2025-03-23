import requests
import os
import json
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

# ساخت URI از اطلاعات محیطی
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "27017")
DB_NAME = os.getenv("DB_NAME", "nexus_ai")

MONGO_URI = f"mongodb://{DB_HOST}:{DB_PORT}"
client = AsyncIOMotorClient(MONGO_URI)
db = client["nexus_aitech"]

# ✅ بارگذاری متغیرهای محیطی با بررسی `.env`
try:
    if os.path.exists(".env"):
        load_dotenv()
    else:
        print("⚠️ فایل .env یافت نشد. برخی مقادیر ممکن است مقداردهی نشده باشند.")
except Exception as e:
    print(f"❌ خطا در بارگذاری .env: {e}")

# ✅ تنظیمات عمومی MVP
try:
    MVP_CONFIG = {
        "DEBUG": os.getenv("DEBUG_MODE", "False").lower() == "true",
        "HOST": os.getenv("HOST", "0.0.0.0"),
        "PORT": int(os.getenv("PORT", 5000)),
        "LOAD_BALANCER": os.getenv("LOAD_BALANCER", "enabled").lower() == "enabled"
    }
except ValueError:
    print("❌ مقدار غیرمعتبر برای PORT. مقدار پیش‌فرض 5000 استفاده می‌شود.")
    MVP_CONFIG = {"DEBUG": False, "HOST": "0.0.0.0", "PORT": 5000, "LOAD_BALANCER": True}

# ✅ مدیریت داینامیک بات‌ها از طریق پایگاه داده یا API
def get_active_bots():
    """📡 دریافت لیست بات‌های فعال از پایگاه داده یا تنظیمات API"""
    try:
        response = requests.get(os.getenv("BOT_CONFIG_API", "http://localhost:5002/api/active_bots"), timeout=5)
        response.raise_for_status()
        return response.json().get("active_bots", [])
    except requests.exceptions.RequestException as e:
        print(f"⚠️ خطا در دریافت لیست بات‌ها از API: {e}")
    return ["cyber_defense", "data_analysis", "fintech", "metaverse", "ai_teacher", "blockchain"]

ACTIVE_BOTS = get_active_bots()

# ✅ تنظیمات بلاکچین (پشتیبانی از چندین شبکه)
ANKR_API_KEY = os.getenv("ANKR_API_KEY")
if not ANKR_API_KEY:
    print("⚠️ کلید API `ANKR_API_KEY` مقداردهی نشده است. اتصال به بلاکچین‌ها ممکن است ناموفق باشد.")

BLOCKCHAIN_APIS = {
    chain: f"https://rpc.ankr.com/{chain}/{ANKR_API_KEY}" if ANKR_API_KEY else None
    for chain in ["ethereum", "bsc", "avalanche", "arbitrum", "solana"]
}

for chain, url in BLOCKCHAIN_APIS.items():
    if not url:
        print(f"⚠️ API برای {chain} مقداردهی نشده است. امکان اتصال وجود ندارد.")

# ✅ تنظیمات APIهای صرافی‌ها و تحلیل داده
EXCHANGE_APIS = {
    "kucoin": os.getenv("KUCOIN_API_KEY"),
    "bitget": os.getenv("BITGET_API_KEY"),
    "bingx": os.getenv("BINGX_API_KEY"),
    "coinmarketcap": os.getenv("COINMARKETCAP_API_KEY"),
}

for exchange, key in EXCHANGE_APIS.items():
    if not key:
        print(f"⚠️ API Key برای {exchange} مقداردهی نشده است.")

NEWS_APIS = {"crypto_panic": os.getenv("CRYPTOPANIC_API_KEY")}

def check_blockchain_status():
    """⛓️ بررسی وضعیت شبکه بلاکچین‌ها"""
    print("⛓️ بررسی وضعیت بلاکچین‌ها...")
    blockchain_status = {}
    for chain, url in BLOCKCHAIN_APIS.items():
        if not url:
            blockchain_status[chain] = "API Key Missing"
            continue
        try:
            response = requests.post(url, json={"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1}, timeout=5)
            response.raise_for_status()
            blockchain_data = response.json()
            latest_block = blockchain_data.get("result", "Unknown")
            latest_block_number = int(latest_block, 16) if latest_block != "Unknown" else "Unknown"
            blockchain_status[chain] = latest_block_number
        except requests.exceptions.RequestException as e:
            blockchain_status[chain] = f"Offline ({e})"
    print(json.dumps(blockchain_status, indent=4, ensure_ascii=False))
    return blockchain_status

if __name__ == "__main__":
    check_blockchain_status()