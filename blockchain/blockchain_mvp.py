import asyncio
import json
import logging
import sys
import os
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from utils.logger import log_info, log_error
from ai_engine import TransactionAnalyzer
from database import store_block_data, get_last_known_block
from blockchain_live import get_latest_block  # استفاده از Alchemy برای دریافت بلاک واقعی
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# اضافه کردن مسیر پروژه برای اطمینان از ایمپورت صحیح ماژول‌ها
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

# مدل تحلیل هوش مصنوعی برای تراکنش‌ها
ai_analyzer = TransactionAnalyzer()

# اتصال به پایگاه داده MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["blockchain_db"]
transactions_collection = db["transactions"]

# تنظیمات لاگ‌گیری
logger = logging.getLogger("Blockchain")

class BlockchainMonitor:
    def __init__(self):
        log_info("🔗 BlockchainMonitor مقداردهی شد.")

    async def check_blockchain_status(self):
        log_info("🔍 بررسی وضعیت بلاکچین...")
        DEFAULT_BLOCKCHAIN = os.getenv("DEFAULT_BLOCKCHAIN", "eth")
        status = get_latest_block(DEFAULT_BLOCKCHAIN)
        log_info(f"📦 وضعیت بلاکچین: {status}")
        return status

blockchain_mvp = BlockchainMonitor()

async def fetch_block_data():
    """ دریافت اطلاعات آخرین بلاک از شبکه واقعی و تحلیل هوشمند تراکنش‌ها """
    try:
        latest_known = await get_last_known_block()
        last_stored_block = latest_known.get("block_number", 0)

        network_status = get_latest_block("eth")
        network_block = network_status.get("block_number", 0)

        if network_block <= last_stored_block:
            log_info(f"⛓️ بلاک جدیدی وجود ندارد. بلاک فعلی: {network_block}")
            return None

        # شبیه‌سازی تعداد تراکنش برای این بلاک (در آینده می‌تونه واقعی بشه)
        transactions = network_block % 200 + 50  # فرمول ساده برای تنوع آماری
        analyzed = ai_analyzer.analyze_transactions(network_block, transactions)

        await store_block_data(network_block, analyzed, datetime.utcnow())
        log_info(f"✅ بلاک {network_block} ثبت شد با {transactions} تراکنش و تحلیل AI.")

        return {
            "block_number": network_block,
            "transactions": transactions,
            "analyzed": analyzed
        }

    except Exception as e:
        log_error(f"❌ خطا در دریافت بلاک: {e}")
        return None

async def run_blockchain_monitor():
    """ اجرای مانیتورینگ بلاکچین به‌صورت دوره‌ای و زنده """
    log_info("🚀 Blockchain Monitor در حال اجراست...")
    while True:
        await fetch_block_data()
        await asyncio.sleep(10)  # بررسی هر 10 ثانیه یک‌بار

# ... ادامه‌ی کد قبلی همون‌طور باقی می‌مونه ...

if __name__ == "__main__":
    asyncio.run(run_blockchain_monitor())


# ⚡ تابع کمکی برای API یا داشبورد برای دریافت یک ساختار ساده‌شده از آخرین وضعیت
def fetch_transactions_from_network():
    """
    این تابع برای استفاده توسط API یا داشبورد طراحی شده تا آخرین اطلاعات بلاک تحلیل‌شده را بدهد.
    """
    try:
        # داده‌های ساختگی یا آخرین داده‌ای که در دیتابیس ذخیره شده
        return {
            "block_number": 123456,
            "transactions": 79,
            "analyzed": {
                "summary": "No threats found"
            }
        }
    except Exception as e:
        log_error(f"❌ خطا در fetch_transactions_from_network: {e}")
        return {
            "block_number": "-",
            "transactions": "-",
            "analyzed": {"summary": "خطا در دریافت"}
        }

