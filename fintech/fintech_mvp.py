import asyncio
import logging
import json
import random
import os
import sys
from datetime import datetime
from utils.logger import log_info, log_error
from ai_engine import TransactionSecurity, FraudDetection
from database import store_transaction, fetch_pending_transactions

# اطمینان از مسیر پروژه
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

# مدل‌های امنیت و تشخیص تقلب
security_model = TransactionSecurity()
fraud_detector = FraudDetection()

# تنظیم لاگر
logger = logging.getLogger("Fintech")

def simulate_financial_transactions(num_transactions=10):
    """شبیه‌سازی تراکنش‌های مالی"""
    transactions = []
    for _ in range(num_transactions):
        transaction = {
            "transaction_id": f"TX_{random.randint(100000, 999999)}",
            "sender": f"user_{random.randint(1, 1000)}",
            "receiver": f"user_{random.randint(1, 1000)}",
            "amount": round(random.uniform(10, 1000), 2),
            "currency": random.choice(["USD", "EUR", "BTC"]),
            "status": "pending",
            "timestamp": datetime.utcnow(),
        }
        transactions.append(transaction)

    logger.info(f"✅ {num_transactions} تراکنش مالی شبیه‌سازی شد.")
    return transactions

async def process_transaction(tx):
    """ پردازش تکی تراکنش """
    try:
        tx_id = tx.get("transaction_id", "UNKNOWN")
        tx["status"] = await security_model.verify_transaction(tx)

        if await fraud_detector.detect_fraud(tx):
            tx["status"] = "Fraud Detected"
            log_error(f"🚨 تراکنش مشکوک به تقلب شناسایی شد! TX ID: {tx_id}")
        else:
            await store_transaction(tx, datetime.now())
            log_info(f"✅ تراکنش ثبت شد: {json.dumps(tx, ensure_ascii=False)}")
    except Exception as e:
        log_error(f"❌ خطا در پردازش تراکنش {tx_id}: {e}")

async def process_transactions():
    """ پردازش لیست تراکنش‌ها به‌صورت همزمان """
    try:
        transactions = await fetch_pending_transactions()

        if not transactions:
            log_info("🚫 هیچ تراکنشی برای پردازش وجود ندارد.")
            return

        # ایمن‌سازی لیست وظایف async
        tasks = []
        for tx in transactions:
            if tx and isinstance(tx, dict):
                tasks.append(process_transaction(tx))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        else:
            log_info("⚠️ تراکنش معتبری برای پردازش یافت نشد.")
    except Exception as e:
        log_error(f"⚠️ خطا در پردازش تراکنش‌ها: {e}")

async def run_continuous_processing():
    """ حلقه پردازش دائمی """
    while True:
        await process_transactions()
        await asyncio.sleep(10)

if __name__ == "__main__":
    log_info("🚀 Fintech Processor در حال راه‌اندازی...")
    try:
        asyncio.run(run_continuous_processing())
    except KeyboardInterrupt:
        log_info("🛑 متوقف شد توسط کاربر.")
    except Exception as e:
        log_error(f"❌ خطای عمومی در اجرای حلقه: {e}")
