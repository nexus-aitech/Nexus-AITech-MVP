import importlib
import time
import logging
from utils.logger import log_info, log_error, log_warning
from market_api import get_live_crypto_price
from price_storage import store_price_data

# 🔹 تعریف پکیج اصلی MVP و ماژول‌های مورد نیاز
modules = [
    "core.core_coordinator_mvp",
    "security.cyber_defense_mvp",
    "analytics.data_analysis_mvp",
    "fintech.fintech_mvp",
    "metaverse.metaverse_mvp",
    "ai_teachers.ai_teacher_mvp",
    "blockchain.blockchain_mvp",
    "ai_engine",  # ✅ اضافه کردن ماژول ai_engine
    "utils.logger",  # ✅ اضافه کردن ماژول logger
    "database",  # ✅ اضافه کردن ماژول database برای مدیریت اطلاعات زنده
]

MAX_RETRIES = 2  # 🔄 حداکثر دو تلاش مجدد برای بارگذاری ماژول‌ها

def load_module(module):
    """بارگذاری و بررسی سلامت هر ماژول"""
    try:
        start_time = time.time()
        importlib.import_module(module)
        load_time = round(time.time() - start_time, 2)
        log_info(f"✅ {module} Loaded Successfully in {load_time} seconds!")
        return True
    except ImportError as e:
        log_error(f"❌ ImportError in {module}: {e}. مسیر ماژول را بررسی کنید.")
    except Exception as e:
        log_error(f"⚠️ Unexpected error in {module}: {e}")
    return False

# 🔥 تلاش برای بارگذاری تمامی ماژول‌ها
failed_modules = []
for module in modules:
    if not load_module(module):
        failed_modules.append(module)

# 🚀 تلاش مجدد برای بارگذاری ماژول‌های ناموفق
for retry in range(MAX_RETRIES):
    if not failed_modules:
        break
    log_warning(f"🔄 تلاش مجدد {retry + 1} برای بارگذاری ماژول‌های ناموفق...")
    for module in failed_modules[:]:
        if load_module(module):
            failed_modules.remove(module)

# 📝 گزارش نهایی بارگذاری ماژول‌ها
if not failed_modules:
    log_info("✅ تمامی ماژول‌ها با موفقیت بارگذاری شدند!")
else:
    log_error(f"❌ ماژول‌های زیر همچنان خطا دارند: {failed_modules}. لطفاً بررسی کنید.")
