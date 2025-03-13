import requests

# آدرس سرور مرکزی (Core Coordinator)
CORE_URL = "http://localhost:5000/api/process"

def detect_threats():
    """ شبیه‌سازی شناسایی تهدیدات اولیه """
    print("🔍 اسکن سیستم برای تهدیدات سایبری...")
    
    # ارسال درخواست به Core Coordinator
    response = requests.post(CORE_URL, json={"bot_name": "cyber_defense"})
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ گزارش امنیتی دریافت شد: {data['response']}")
    else:
        print("❌ خطا در دریافت گزارش امنیتی!")

if __name__ == "__main__":
    detect_threats()

# Cyber Defense Mvp
print('Executing cyber_defense_mvp.py')
