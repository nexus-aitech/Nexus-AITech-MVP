import logging
import os

# مسیر ذخیره‌سازی لاگ‌ها
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "mvp.log")

# اگر فولدر لاگ وجود نداشت، ایجاد شود
os.makedirs(LOG_DIR, exist_ok=True)

# تنظیمات Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),  # ذخیره در فایل
        logging.StreamHandler()  # نمایش در ترمینال
    ]
)

def log_info(message):
    """ثبت لاگ اطلاعاتی"""
    logging.info(message)

def log_warning(message):
    """ثبت لاگ هشدار"""
    logging.warning(message)

def log_error(message):
    """ثبت لاگ خطا"""
    logging.error(message)

if __name__ == "__main__":
    log_info("✅ Logger آماده استفاده است!")

# Logger
print('Executing logger.py')
