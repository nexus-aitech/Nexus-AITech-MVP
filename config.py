import asyncio
import os
import json
import requests
import redis
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# 📦 بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()
if not os.path.exists(".env"):
    print("⚠️ فایل .env یافت نشد. برخی تنظیمات ممکن است ناقص باشند.")

# ✅ تنظیمات پایگاه داده MongoDB
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "27017")
DB_NAME = os.getenv("DB_NAME", "nexus_aitech")

MONGO_URI = f"mongodb://{DB_HOST}:{DB_PORT}"
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# ✅ تنظیمات Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

try:
    redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    redis_client.ping()
    print("✅ اتصال Redis برقرار شد.")
except Exception as e:
    print(f"❌ خطا در اتصال به Redis: {e}")
    redis_client = None

# ✅ تنظیمات مربوط به اجرای MVP
try:
    MVP_CONFIG = {
        "DEBUG": os.getenv("DEBUG_MODE", "false").lower() == "true",
        "HOST": os.getenv("HOST", "0.0.0.0"),
        "PORT": int(os.getenv("PORT", 8050)),
        "LOAD_BALANCER": os.getenv("LOAD_BALANCER", "enabled").lower() == "enabled"
    }
except Exception as e:
    print(f"❌ خطا در تنظیمات MVP: {e}")
    MVP_CONFIG = {"DEBUG": False, "HOST": "0.0.0.0", "PORT": 8050, "LOAD_BALANCER": True}

# ✅ دریافت لیست بات‌های فعال از API یا بازگشت به حالت پیش‌فرض
def get_active_bots():
    try:
        api_url = os.getenv("BOT_CONFIG_API", "http://app:8000/api/active_bots")
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        return response.json().get("active_bots", [])
    except requests.RequestException as e:
        print(f"⚠️ دریافت لیست بات‌ها از API ناموفق بود: {e}")
        return ["cyber_defense", "data_analysis", "fintech", "metaverse", "ai_teacher", "blockchain"]

ACTIVE_BOTS = get_active_bots()

# ✅ تنظیمات اتصال به بلاکچین‌های مختلف با استفاده از ANKR
ANKR_API_KEY = os.getenv("ANKR_API_KEY")
SUPPORTED_CHAINS = ["ethereum", "bsc", "avalanche", "arbitrum", "solana"]

BLOCKCHAIN_APIS = {
    chain: f"https://rpc.ankr.com/{chain}/{ANKR_API_KEY}" if ANKR_API_KEY else None
    for chain in SUPPORTED_CHAINS
}

for chain, url in BLOCKCHAIN_APIS.items():
    if not url:
        print(f"⚠️ API برای شبکه {chain} مقداردهی نشده است.")

# ✅ کلیدهای API برای صرافی‌ها
EXCHANGE_APIS = {
    "kucoin": os.getenv("KUCOIN_API_KEY"),
    "bitget": os.getenv("BITGET_API_KEY"),
    "bingx": os.getenv("BINGX_API_KEY"),
    "coinmarketcap": os.getenv("COINMARKETCAP_API_KEY"),
}

for name, key in EXCHANGE_APIS.items():
    if not key:
        print(f"⚠️ کلید API برای {name} موجود نیست.")

# ✅ کلید API برای اخبار کریپتو
NEWS_APIS = {
    "crypto_panic": os.getenv("CRYPTOPANIC_API_KEY")
}

# ✅ بررسی وضعیت شبکه‌های بلاکچین
def check_blockchain_status():
    print("⛓️ بررسی وضعیت بلاکچین‌ها...")
    status = {}

    for chain, url in BLOCKCHAIN_APIS.items():
        if not url:
            status[chain] = "❌ API Key Missing"
            continue

        try:
            response = requests.post(
                url,
                json={
                    "jsonrpc": "2.0",
                    "method": "eth_blockNumber",
                    "params": [],
                    "id": 1
                },
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            block_hex = data.get("result")
            status[chain] = int(block_hex, 16) if block_hex else "⛔ Unknown"
        except Exception as e:
            status[chain] = f"🔌 Offline ({str(e)})"

def safe_json_dumps(data):
    def convert(o):
        if isinstance(o, ObjectId):
            return str(o)
        return str(o)  # تبدیل fallback برای هر نوع ناشناس
    return json.dumps(data, default=convert, indent=4, ensure_ascii=False)

    print(safe_json_dumps(status))
    return status

# ✅ اجرای بررسی فقط در حالت مستقیم
if __name__ == "__main__":
    check_blockchain_status()
    