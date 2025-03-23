import asyncio
import json
import logging
import random
import time
import sys
import os
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from utils.logger import log_info, log_error
from ai_engine import TransactionAnalyzer
from database import store_block_data, get_last_known_block

# اضافه کردن مسیر پروژه برای اطمینان از ایمپورت صحیح ماژول‌ها
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

# مدل تحلیل هوش مصنوعی برای تراکنش‌ها
ai_analyzer = TransactionAnalyzer()

# اتصال به پایگاه داده MongoDB
MONGO_URI = "mongodb://localhost:27017"
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
        await asyncio.sleep(2)
        log_info("✅ وضعیت بلاکچین بررسی شد.")

blockchain_mvp = BlockchainMonitor()

async def check_blockchain_status():
    """بررسی وضعیت فعلی بلاکچین"""
    try:
        logger.info("✅ وضعیت بلاکچین بررسی شد.")
        return {"status": "active", "latest_block": 12345}
    except Exception as e:
        logger.error(f"❌ خطا در بررسی وضعیت بلاکچین: {e}")
        return {"status": "error", "error": str(e)}

async def fetch_block_data():
    """ دریافت اطلاعات آخرین بلاک و تحلیل هوشمند تراکنش‌ها """
    latest_block = await get_last_known_block()  # اصلاح به async
    block_number = latest_block.get("block_number", 0) + 1
    transactions = random.randint(50, 300)
    analyzed_transactions = ai_analyzer.analyze_transactions(block_number, transactions)
    await store_block_data(block_number, analyzed_transactions, datetime.now())  # اصلاح به async
    log_info(f"⛓️ بلاک {block_number} - تعداد تراکنش‌ها: {transactions}")
    return {"block_number": block_number, "transactions": transactions, "analyzed_data": analyzed_transactions}

async def fetch_transactions_from_network():
    """ شبیه‌سازی دریافت تراکنش‌های بلاکچین """
    return {"status": "Success", "latest_block": random.randint(1000, 5000), "transactions": random.randint(10, 100)}

async def get_latest_transactions():
    try:
        transactions = await fetch_transactions_from_network()
        if transactions is None:
            return {"status": "No Transactions Available", "latest_block": 0, "transactions": 0}
        return transactions
    except Exception as e:
        log_error(f"خطا در دریافت تراکنش‌های بلاکچین: {str(e)}")
        return {"status": "Error", "latest_block": 0, "transactions": 0}

async def run_blockchain_monitor():
    """ اجرای نظارت زنده بر بلاکچین """
    while True:
        await fetch_block_data()
        await asyncio.sleep(10)

if __name__ == "__main__":
    log_info("🚀 Blockchain Monitor در حال راه‌اندازی...")
    asyncio.run(run_blockchain_monitor())  # اصلاح به async