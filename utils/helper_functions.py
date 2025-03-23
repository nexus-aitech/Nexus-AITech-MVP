import asyncio
import json
import requests
import sys
import os
from utils.logger import log_info, log_error

# اضافه کردن مسیر پروژه برای اطمینان از ایمپورت صحیح ماژول‌ها
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

def format_json(data):
    """📜 تبدیل داده‌های JSON به فرمت خوانا"""
    return json.dumps(data, indent=4, ensure_ascii=False)

def send_request(url, method="GET", payload=None, headers=None, auth_token=None):
    """📡 ارسال درخواست HTTP با مدیریت پیشرفته"""
    try:
        log_info(f"📡 ارسال {method} به {url}")
        
        # تنظیم هدرها
        request_headers = {"Content-Type": "application/json"}
        if headers:
            request_headers.update(headers)
        if auth_token:
            request_headers["Authorization"] = f"Bearer {auth_token}"
        
        # ارسال درخواست با متد مشخص شده
        response = requests.request(method, url, json=payload, headers=request_headers, timeout=10)
        response.raise_for_status()
        
        # بررسی نوع پاسخ دریافتی
        try:
            return response.json()
        except json.JSONDecodeError:
            log_error("❌ خطا: پاسخ دریافت‌شده JSON معتبر نیست!")
            return None
    
    except requests.exceptions.Timeout:
        log_error(f"⏳ خطا: درخواست به {url} تایم‌اوت شد.")
        return None
    except requests.exceptions.ConnectionError:
        log_error(f"🚨 خطا: ارتباط با {url} امکان‌پذیر نیست!")
        return None
    except requests.exceptions.RequestException as e:
        log_error(f"❌ خطای درخواست: {e}")
        return None

if __name__ == "__main__":
    log_info("✅ Helper Functions آماده استفاده است!")