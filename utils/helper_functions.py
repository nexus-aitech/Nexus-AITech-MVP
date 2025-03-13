import json
import requests
from logger import log_info, log_error

def format_json(data):
    """تبدیل داده‌های JSON به فرمت خوانا"""
    return json.dumps(data, indent=4, ensure_ascii=False)

def send_request(url, payload=None):
    """ارسال درخواست HTTP و مدیریت پاسخ"""
    try:
        log_info(f"📡 ارسال درخواست به {url}")
        response = requests.post(url, json=payload) if payload else requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        log_error(f"❌ خطای درخواست: {e}")
        return None

if __name__ == "__main__":
    log_info("✅ Helper Functions آماده استفاده است!")

# Helper Functions
print('Executing helper_functions.py')
