import requests
import random

# آدرس سرور مرکزی (Core Coordinator)
CORE_URL = "http://localhost:5000/api/process"

def process_transaction():
    """ شبیه‌سازی یک تراکنش ساده NXAIT """
    print("💳 در حال انجام تراکنش...")

    # اطلاعات تراکنش آزمایشی
    transaction_data = {
        "from": "User123",
        "to": "Merchant456",
        "amount": f"{random.randint(1, 500)} NXAIT",
        "status": "Pending"
    }

    print(f"🔹 جزئیات تراکنش: {transaction_data}")

    # ارسال درخواست به Core Coordinator برای تأیید
    response = requests.post(CORE_URL, json={"bot_name": "fintech"})
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ تأیید تراکنش از Core Coordinator: {data['response']}")
    else:
        print("❌ خطا در تأیید تراکنش!")

if __name__ == "__main__":
    process_transaction()

# Fintech Mvp
print('Executing fintech_mvp.py')
