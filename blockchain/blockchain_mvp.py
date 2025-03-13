import requests

# آدرس سرور مرکزی (Core Coordinator)
CORE_URL = "http://localhost:5000/api/process"

# استفاده از API رایگان برای دریافت وضعیت شبکه اتریوم (می‌توان تغییر داد)
ETHERSCAN_API = "https://api.blockcypher.com/v1/eth/main"

def check_blockchain_status():
    """ بررسی وضعیت شبکه بلاکچین """
    print("⛓️ در حال ارتباط با بلاکچین...")

    try:
        response = requests.get(ETHERSCAN_API)
        if response.status_code == 200:
            blockchain_data = response.json()
            latest_block = blockchain_data.get("height", "نامشخص")
            print(f"🔗 آخرین بلاک: {latest_block}")

            # ارسال داده به Core Coordinator
            response = requests.post(CORE_URL, json={"bot_name": "blockchain"})
            if response.status_code == 200:
                data = response.json()
                print(f"✅ پاسخ Core Coordinator: {data['response']}")
            else:
                print("❌ خطا در ارسال اطلاعات به Core Coordinator!")

        else:
            print("❌ خطا در دریافت داده از بلاکچین!")

    except Exception as e:
        print(f"⚠️ خطای اتصال: {e}")

if __name__ == "__main__":
    check_blockchain_status()

# Blockchain Mvp
print('Executing blockchain_mvp.py')
