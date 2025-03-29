import asyncio
import json
import os
import logging
import pymongo
from bson import ObjectId
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# بارگذاری متغیرهای محیطی
load_dotenv()

# تنظیمات لاگ‌گیری
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Database")

# اتصال به پایگاه داده MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["my_database"]

# تعریف کلکشن‌ها
data_collection = db["real_data"]
students_collection = db["students"]
lesson_logs_collection = db["lesson_logs"]
blocks_collection = db["block_data"]
metaverse_collection = db["metaverse_data"]

# Utility function for ObjectId conversion
def convert_objectid_to_str(document):
    if isinstance(document, dict):
        return {k: str(v) if isinstance(v, ObjectId) else v for k, v in document.items()}
    return document

async def fetch_real_data(query={}):
    try:
        cursor = data_collection.find(query)
        data = await cursor.to_list(length=None)
        logger.info("✅ داده‌ها با موفقیت دریافت شدند.")
        return data
    except Exception as e:
        logger.error(f"❌ خطا در دریافت داده‌ها: {e}")
        return []

async def store_transaction(transaction_data):
    try:
        transactions_collection = db["transactions"]
        transaction_data["timestamp"] = datetime.utcnow().isoformat()
        result = await transactions_collection.insert_one(transaction_data)
        transaction_data["_id"] = str(result.inserted_id)  # تبدیل ObjectId به str
        safe_data = convert_objectid_to_str(transaction_data)
        logger.info(f"✅ تراکنش ذخیره شد: {json.dumps(safe_data, ensure_ascii=False)}")
    except Exception as e:
        logger.error(f"❌ خطا در ذخیره تراکنش: {e}")

async def log_threat(threat_data):
    try:
        threats_collection = db["cyber_threats"]
        threat_data["timestamp"] = datetime.utcnow().isoformat()
        result = await threats_collection.insert_one(threat_data)
        threat_data["_id"] = str(result.inserted_id)  # تبدیل ObjectId به str
        safe_data = convert_objectid_to_str(threat_data)
        logger.info(f"✅ تهدید سایبری ثبت شد: {json.dumps(safe_data, ensure_ascii=False)}")
    except Exception as e:
        logger.error(f"❌ خطا در ثبت تهدید سایبری: {e}")

async def fetch_pending_transactions():
    try:
        transactions_collection = db["transactions"]
        cursor = transactions_collection.find({"status": "pending"})
        pending_transactions = await cursor.to_list(length=None)
        logger.info(f"✅ {len(pending_transactions)} تراکنش در انتظار پردازش دریافت شد.")
        return pending_transactions
    except Exception as e:
        logger.error(f"❌ خطا در دریافت تراکنش‌های معلق: {e}")
        return []

async def block_ip(ip_address):
    try:
        blocked_ips_collection = db["blocked_ips"]
        await blocked_ips_collection.insert_one({"ip": ip_address, "blocked_at": datetime.utcnow().isoformat()})
        logger.info(f"✅ آی‌پی {ip_address} مسدود شد.")
    except Exception as e:
        logger.error(f"❌ خطا در مسدود کردن آی‌پی {ip_address}: {e}")

async def store_analysis_result(analysis_data):
    try:
        analysis_results_collection = db["analysis_results"]
        analysis_data["timestamp"] = datetime.utcnow().isoformat()
        await analysis_results_collection.insert_one(analysis_data)

        # اضافه کردن لاگ تمیز با ObjectId تبدیل‌شده
        safe_analysis = convert_objectid_to_str(analysis_data)
        logger.info(f"✅ نتیجه تحلیل داده‌ها ذخیره شد: {json.dumps(safe_analysis, ensure_ascii=False)}")
    except Exception as e:
        logger.error(f"❌ خطا در ذخیره نتیجه تحلیل داده‌ها: {e}")

async def get_active_students():
    try:
        cursor = students_collection.find({"active": True}, {"_id": 0, "student_id": 1, "name": 1})
        students = await cursor.to_list(length=100)
        logger.info(f"✅ {len(students)} دانش‌آموز فعال دریافت شد.")
        return students
    except Exception as e:
        logger.error(f"❌ خطا در دریافت دانش‌آموزان فعال: {e}")
        return []

async def log_lesson_activity(student_id, lesson):
    try:
        await lesson_logs_collection.insert_one({
            "student_id": student_id,
            "lesson": lesson,
            "timestamp": datetime.utcnow().isoformat()
        })
        logger.info(f"✅ فعالیت درسی برای دانش‌آموز {student_id} در درس {lesson} ثبت شد.")
    except Exception as e:
        logger.error(f"❌ خطا در ثبت فعالیت درسی: {e}")

async def store_block_data(block):
    try:
        block["timestamp"] = datetime.utcnow().isoformat()
        await blocks_collection.insert_one(block)
        logger.info(f"✅ بلاک با شناسه {block.get('block_hash')} ذخیره شد.")
    except Exception as e:
        logger.error(f"❌ خطا در ذخیره بلاک: {e}")

async def get_last_known_block():
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
    try:
        cursor = metaverse_collection.find().sort("timestamp", pymongo.DESCENDING).limit(10)
        metaverse_data = await cursor.to_list(length=10)
        logger.info(f"✅ {len(metaverse_data)} رکورد متاورس دریافت شد.")
        return metaverse_data
    except Exception as e:
        logger.error(f"❌ خطا در دریافت داده‌های متاورس: {e}")
        return []

async def store_metaverse_activity(activity):
    try:
        activity["timestamp"] = datetime.utcnow().isoformat()
        activity_data = activity.copy()

        if "_id" in activity_data:
            existing = await metaverse_collection.find_one({"_id": activity_data["_id"]})
            if existing:
                print(f"[⚠️] رکورد متاورس با _id تکراری یافت شد: {activity_data['_id']}")
            else:
                if isinstance(activity_data["_id"], ObjectId):
                    print(f"[INFO] در حال درج رکورد متاورس با _id: {str(activity_data['_id'])}")
                await metaverse_collection.insert_one(activity_data)
        else:
            print("[⚠️] فعالیت متاورس بدون _id ارسال شده است.")

        # لاگ موفقیت
        safe_activity = convert_objectid_to_str(activity_data)
        print(f"✅ فعالیت متاورس ذخیره شد: {json.dumps(safe_activity, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ خطا در ذخیره فعالیت متاورس: {e}")

if __name__ == "__main__":
    async def main():
        students = await get_active_students()
        print("👨‍🎓 لیست دانش‌آموزان فعال:", students)

        await log_lesson_activity("S12345", "Mathematics")

        sample_block = {"block_hash": "abc123", "transactions": 15, "miner": "0xMinerAddress"}
        await store_block_data(sample_block)

        last_block = await get_last_known_block()
        print("🔍 آخرین بلاک ذخیره شده:", last_block)

        metaverse_data = await fetch_metaverse_data()
        print("🌐 داده‌های متاورس:", metaverse_data)

        sample_activity = {"user_id": "U12345", "action": "Virtual Land Purchase", "amount": 1000}
        await store_metaverse_activity(sample_activity)

    asyncio.run(main())

__all__ = [
    "get_active_students",
    "log_lesson_activity",
    "store_block_data",
    "get_last_known_block",
    "fetch_metaverse_data",
    "store_metaverse_activity",
    "store_transaction",
    "log_threat",
    "fetch_pending_transactions",
    "block_ip",
    "store_analysis_result",
    "fetch_real_data"
]
