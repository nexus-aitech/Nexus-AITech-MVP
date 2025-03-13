import requests
import random

# آدرس سرور مرکزی (Core Coordinator)
CORE_URL = "http://localhost:5000/api/process"

def connect_to_metaverse():
    """ شبیه‌سازی اتصال به متاورس """
    print("🌐 در حال برقراری ارتباط با سرور متاورس...")

    # اطلاعات متاورس آزمایشی
    metaverse_data = {
        "status": "Connecting",
        "active_users": random.randint(50, 500),
        "server": "MetaWorld-1"
    }

    print(f"🔹 اطلاعات متاورس: {metaverse_data}")

    # ارسال درخواست به Core Coordinator
    response = requests.post(CORE_URL, json={"bot_name": "metaverse"})
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ پاسخ Core Coordinator: {data['response']}")
    else:
        print("❌ خطا در دریافت پاسخ از Core Coordinator!")

if __name__ == "__main__":
    connect_to_metaverse()

# Metaverse Mvp
print('Executing metaverse_mvp.py')
