import asyncio
import os
import logging
import pymongo
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی
load_dotenv()

# تنظیمات لاگ‌گیری
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Database")

# اتصال به پایگاه داده MongoDB (با استفاده از نسخه‌ی Asynchronous برای مقیاس‌پذیری بالا)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["my_database"]  # ✅ تنظیم پایگاه داده از متغیر محیطی

data_collection = db["real_data"]  # ✅ تعریف متغیر در سطح گلوبال برای رفع خطا
students_collection = db["students"]
lesson_logs_collection = db["lesson_logs"]
blocks_collection = db["block_data"]
metaverse_collection = db["metaverse_data"]  # ✅ مجموعه جدید برای متاورس

async def fetch_real_data(query={}):
    """دریافت داده‌های واقعی از پایگاه داده"""
    try:
        cursor = data_collection.find(query)
        data = await cursor.to_list(length=None)  # ✅ استفاده از to_list برای تبدیل کرسر به لیست
        logger.info("✅ داده‌ها با موفقیت دریافت شدند.")
        return data
    except Exception as e:
        logger.error(f"❌ خطا در دریافت داده‌ها: {e}")
        return []

async def store_transaction(transaction_data):
    """ذخیره تراکنش‌ها در پایگاه داده MongoDB"""
    try:
        transactions_collection = db["transactions"]
        transaction_data["timestamp"] = datetime.utcnow()
        transactions_collection.insert_one(transaction_data)
        logger.info("✅ تراکنش ذخیره شد.")
    except Exception as e:
        logger.error(f"❌ خطا در ذخیره تراکنش: {e}")

async def log_threat(threat_data):
    """ذخیره اطلاعات تهدیدات سایبری در پایگاه داده"""
    try:
        threats_collection = db["cyber_threats"]
        threat_data["timestamp"] = datetime.utcnow()
        threats_collection.insert_one(threat_data)
        logger.info("✅ تهدید سایبری ثبت شد.")
    except Exception as e:
        logger.error(f"❌ خطا در ثبت تهدید سایبری: {e}")

async def fetch_pending_transactions():
    """دریافت تراکنش‌های در انتظار پردازش از پایگاه داده"""
    try:
        transactions_collection = db["transactions"]
        pending_transactions = list(transactions_collection.find({"status": "pending"}))
        logger.info(f"✅ {len(pending_transactions)} تراکنش در انتظار پردازش دریافت شد.")
        return pending_transactions
    except Exception as e:
        logger.error(f"❌ خطا در دریافت تراکنش‌های معلق: {e}")
        return []

async def block_ip(ip_address):
    """مسدود کردن یک آی‌پی مشکوک و ثبت آن در پایگاه داده"""
    try:
        blocked_ips_collection = db["blocked_ips"]
        blocked_ips_collection.insert_one({"ip": ip_address, "blocked_at": datetime.utcnow()})
        logger.info(f"✅ آی‌پی {ip_address} مسدود شد.")
    except Exception as e:
        logger.error(f"❌ خطا در مسدود کردن آی‌پی {ip_address}: {e}")

async def store_analysis_result(analysis_data):
    """ذخیره نتایج تحلیل داده‌ها در پایگاه داده"""
    try:
        analysis_results_collection = db["analysis_results"]
        analysis_data["timestamp"] = datetime.utcnow()
        analysis_results_collection.insert_one(analysis_data)
        logger.info("✅ نتیجه تحلیل داده‌ها ذخیره شد.")
    except Exception as e:
        logger.error(f"❌ خطا در ذخیره نتیجه تحلیل داده‌ها: {e}")

async def get_active_students():
    """دریافت لیست دانش‌آموزان فعال از پایگاه داده با پردازش موازی"""
    try:
        students_cursor = students_collection.find({"active": True}, {"_id": 0, "student_id": 1, "name": 1})
        students = await students_cursor.to_list(length=100)
        logger.info(f"✅ {len(students)} دانش‌آموز فعال دریافت شد.")
        return students
    except Exception as e:
        logger.error(f"❌ خطا در دریافت دانش‌آموزان فعال: {e}")
        return []

async def log_lesson_activity(student_id, lesson):
    """ثبت فعالیت درسی دانش‌آموز به‌صورت زنده در پایگاه داده"""
    try:
        await lesson_logs_collection.insert_one({
            "student_id": student_id,
            "lesson": lesson,
            "timestamp": datetime.utcnow()
        })
        logger.info(f"✅ فعالیت درسی برای دانش‌آموز {student_id} در درس {lesson} ثبت شد.")
    except Exception as e:
        logger.error(f"❌ خطا در ثبت فعالیت درسی: {e}")

async def store_block_data(block):
    """ذخیره اطلاعات بلاک‌های بلاکچین در پایگاه داده"""
    try:
        block["timestamp"] = datetime.utcnow()
        await blocks_collection.insert_one(block)
        logger.info(f"✅ بلاک با شناسه {block.get('block_hash')} در پایگاه داده ذخیره شد.")
    except Exception as e:
        logger.error(f"❌ خطا در ذخیره بلاک: {e}")

async def get_last_known_block():
    """دریافت آخرین بلاک ذخیره‌شده در پایگاه داده"""
    try:
        last_block = await blocks_collection.find_one(sort=[("timestamp", pymongo.DESCENDING)])
        if last_block:
            logger.info(f"✅ آخرین بلاک دریافت شد: {last_block.get('block_hash')}")
            return last_block
        else:
            logger.warning("⚠️ هیچ بلاکی در پایگاه داده یافت نشد.")
            return None
    except Exception as e:
        logger.error(f"❌ خطا در دریافت آخرین بلاک: {e}")
        return None

async def fetch_metaverse_data():
    """دریافت داده‌های متاورس از پایگاه داده"""
    try:
        cursor = metaverse_collection.find().sort("timestamp", pymongo.DESCENDING).limit(10)
        metaverse_data = await cursor.to_list(length=10)
        logger.info(f"✅ {len(metaverse_data)} رکورد متاورس دریافت شد.")
        return metaverse_data
    except Exception as e:
        logger.error(f"❌ خطا در دریافت داده‌های متاورس: {e}")
        return []

async def store_metaverse_activity(activity):
    """ذخیره فعالیت متاورس در پایگاه داده"""
    try:
        activity["timestamp"] = datetime.utcnow()
        await metaverse_collection.insert_one(activity)
        logger.info(f"✅ فعالیت متاورس با شناسه {activity.get('user_id')} ذخیره شد.")
    except Exception as e:
        logger.error(f"❌ خطا در ذخیره فعالیت متاورس: {e}")

if __name__ == "__main__":
    async def main():
        # تست دریافت دانش‌آموزان فعال
        students = await get_active_students()
        print("👨‍🎓 لیست دانش‌آموزان فعال:", students)
        
        # تست ثبت فعالیت درسی برای اجرای زنده
        await log_lesson_activity("S12345", "Mathematics")
        
        # تست ذخیره بلاک در پایگاه داده
        sample_block = {"block_hash": "abc123", "transactions": 15, "miner": "0xMinerAddress"}
        await store_block_data(sample_block)
        
        # تست دریافت آخرین بلاک
        last_block = await get_last_known_block()
        print("🔍 آخرین بلاک ذخیره شده:", last_block)
        
        # تست دریافت داده‌های متاورس
        metaverse_data = await fetch_metaverse_data()
        print("🌐 داده‌های متاورس:", metaverse_data)
        
        # تست ذخیره فعالیت متاورس
        sample_activity = {"user_id": "U12345", "action": "Virtual Land Purchase", "amount": 1000}
        await store_metaverse_activity(sample_activity)
    
    asyncio.run(main())
    
# اطمینان از اینکه توابع در ماژول لود شده‌اند
__all__ = ["get_active_students", "log_lesson_activity", "store_block_data", "get_last_known_block", "fetch_metaverse_data", "store_metaverse_activity", "get_live_crypto_price"]