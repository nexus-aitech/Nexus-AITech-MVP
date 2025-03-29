import asyncio
import logging
import os
import sys
import json
import re
import unicodedata
from logging.handlers import RotatingFileHandler

# 📁 مسیر ذخیره‌سازی لاگ‌ها
LOG_DIR = os.path.join(os.getcwd(), "logs")
LOG_FILE = os.path.join(LOG_DIR, "mvp.log")

# 📌 ایجاد پوشه لاگ در صورت نبود
try:
    os.makedirs(LOG_DIR, exist_ok=True)
except OSError as e:
    print(f"❌ خطا در ایجاد دایرکتوری لاگ‌ها: {e}")
    sys.exit(1)

# 🔧 تنظیمات Logger
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# 🌀 چرخش لاگ برای جلوگیری از افزایش حجم
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8")
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.INFO)

# 🧠 ساخت آبجکت logger
logger = logging.getLogger("MVP_Logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 🌐 اطمینان از پشتیبانی کامل UTF-8 در محیط اجرا
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "replace")
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "replace")
except Exception:
    pass

# ✅ تابع حذف ایموجی‌ها و کاراکترهای غیرقابل چاپ برای جلوگیری از مشکلات لاگ
def remove_special_chars(text):
    if not isinstance(text, str):
        text = str(text)  # تبدیل به رشته اگر نبود
    text = ''.join(c for c in text if unicodedata.category(c)[0] != 'C')  # حذف کاراکترهای کنترلی
    return text.encode("utf-8", "ignore").decode("utf-8")  # حذف کاراکترهای غیرقابل نمایش

# ✅ توابع ثبت لاگ در فرمت JSON، بدون ایموجی و با هندل کردن ObjectId
def log_info(message):
    log_data = {"level": "INFO", "message": remove_special_chars(str(message))}
    logger.info(json.dumps(log_data, ensure_ascii=False, default=str))

def log_debug(message):
    log_data = {"level": "DEBUG", "message": remove_special_chars(str(message))}
    logger.debug(json.dumps(log_data, ensure_ascii=False, default=str))

def log_warning(message):
    log_data = {"level": "WARNING", "message": remove_special_chars(str(message))}
    logger.warning(json.dumps(log_data, ensure_ascii=False, default=str))

def log_error(message):
    log_data = {"level": "ERROR", "message": remove_special_chars(str(message))}
    logger.error(json.dumps(log_data, ensure_ascii=False, default=str))

def log_critical(message):
    log_data = {"level": "CRITICAL", "message": remove_special_chars(str(message))}
    logger.critical(json.dumps(log_data, ensure_ascii=False, default=str))

# ✅ تست محلی اگر مستقیم اجرا شود
if __name__ == "__main__":
    logger.info("✅ Logger آماده استفاده به‌صورت آبجکت است.")
    log_info("🎯 شروع تست جهانی Logger")
    log_debug("🛠️ Debug فعال شد")
    log_warning("⚠️ هشدار امنیتی")
    log_error("❌ خطای بحرانی")
    log_critical("🚨 خطای سطح بالا")
    print("📄 فایل لاگ در مسیر logs/mvp.log ذخیره شد.")
