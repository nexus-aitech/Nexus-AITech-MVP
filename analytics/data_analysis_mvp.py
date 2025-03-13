import requests
import random

# آدرس سرور مرکزی (Core Coordinator)
CORE_URL = "http://localhost:5000/api/process"

def analyze_data():
    """ شبیه‌سازی تحلیل داده‌های خام """
    print("📊 پردازش و تحلیل داده‌های اولیه...")

    # داده‌های آزمایشی برای تحلیل
    sample_data = {
        "users": random.randint(1000, 5000),
        "transactions": random.randint(100, 1000),
        "error_logs": random.randint(0, 10)
    }

    print(f"🔹 داده‌های پردازش‌شده: {sample_data}")

    # ارسال درخواست به Core Coordinator
    response = requests.post(CORE_URL, json={"bot_name": "data_analysis"})
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ گزارش تحلیل دریافت شد: {data['response']}")
    else:
        print("❌ خطا در دریافت پاسخ از Core Coordinator!")

if __name__ == "__main__":
    analyze_data()

# Data Analysis Mvp
print('Executing data_analysis_mvp.py')
