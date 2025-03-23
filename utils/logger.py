import asyncio
import logging
import os
import sys
import json
import re
from logging.handlers import RotatingFileHandler

# 🔹 مسیر ذخیره‌سازی لاگ‌ها
LOG_DIR = os.path.join(os.getcwd(), "logs")
LOG_FILE = os.path.join(LOG_DIR, "mvp.log")

# ✅ اگر فولدر لاگ وجود نداشت، ایجاد شود
try:
    os.makedirs(LOG_DIR, exist_ok=True)
except OSError as e:
    print(f"❌ خطا در ایجاد دایرکتوری لاگ‌ها: {e}")
    sys.exit(1)

# ✅ تنظیمات Logger برای اجرای زنده
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# 📌 **چرخش لاگ‌ها برای جلوگیری از حجم بالا**
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8")
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.DEBUG)

# 📡 نمایش لاگ‌ها در ترمینال
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.INFO)

# 🔥 تنظیم Logger اصلی
logger = logging.getLogger("MVP_Logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# ✅ **تنظیم خروجی برای UTF-8 (حل مشکل `UnicodeEncodeError` در ویندوز)**
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

# ✅ **حذف ایموجی‌ها قبل از ثبت لاگ برای جلوگیری از `UnicodeEncodeError`**
def remove_emojis(text):
    emoji_pattern = re.compile("[" 
                               u"\U0001F600-\U0001F64F"  # ایموجی‌های چهره‌ای
                               u"\U0001F300-\U0001F5FF"  # نمادها و اشیا
                               u"\U0001F680-\U0001F6FF"  # وسایل نقلیه و اماکن
                               u"\U0001F700-\U0001F77F"  # نمادهای علمی
                               u"\U0001F780-\U0001F7FF"  # نمادهای مختلف
                               u"\U0001F800-\U0001F8FF"  # نمادهای خاص
                               u"\U0001F900-\U0001F9FF"  # ایموجی‌های افراد و ژست‌ها
                               u"\U0001FA00-\U0001FA6F"  # اشیا و حیوانات
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# ✅ **اصلاح توابع لاگ‌گذاری برای حذف ایموجی‌ها و ثبت لاگ در فرمت JSON**
def log_info(message):
    """ثبت لاگ اطلاعاتی"""
    log_data = {"level": "INFO", "message": remove_emojis(message)}
    logger.info(json.dumps(log_data, ensure_ascii=False))

def log_debug(message):
    """ثبت لاگ دیباگ"""
    log_data = {"level": "DEBUG", "message": remove_emojis(message)}
    logger.debug(json.dumps(log_data, ensure_ascii=False))

def log_warning(message):
    """ثبت لاگ هشدار"""
    log_data = {"level": "WARNING", "message": remove_emojis(message)}
    logger.warning(json.dumps(log_data, ensure_ascii=False))

def log_error(message):
    """ثبت لاگ خطا"""
    log_data = {"level": "ERROR", "message": remove_emojis(message)}
    logger.error(json.dumps(log_data, ensure_ascii=False))

def log_critical(message):
    """ثبت لاگ بحرانی"""
    log_data = {"level": "CRITICAL", "message": remove_emojis(message)}
    logger.critical(json.dumps(log_data, ensure_ascii=False))

if __name__ == "__main__":
    log_info("✅ Logger برای اجرای زنده آماده است!")
    log_debug("🐞 این یک لاگ Debug است.")
    log_warning("⚠️ تست هشدار لاگ")
    log_error("❌ تست خطای لاگ")
    log_critical("🔥 تست لاگ بحرانی")

# 🖥 نمایش لاگ اولیه
print("Logger برای ثبت لاگ‌ها آماده است!")