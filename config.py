import os

# تنظیمات عمومی MVP
MVP_CONFIG = {
    "DEBUG": True,  # فعال/غیرفعال کردن حالت دیباگ
    "HOST": "0.0.0.0",  # آدرس اجرای سرور
    "PORT": 5000,  # پورت پیش‌فرض
}

# تنظیمات API برای ارتباط با بلاکچین (در صورت داشتن API Key واقعی اینجا قرار بده)
BLOCKCHAIN_API = {
    "ETHERSCAN_URL": "https://api.blockcypher.com/v1/eth/main",
    "API_KEY": os.getenv("BLOCKCHAIN_API_KEY", "YOUR_FREE_API_KEY"),  # استفاده از متغیر محیطی یا مقدار پیش‌فرض
}

# لیست بات‌های موجود در MVP
ACTIVE_BOTS = [
    "core_coordinator",
    "cyber_defense",
    "data_analysis",
    "fintech",
    "metaverse",
    "ai_teacher",
    "blockchain"
]

print("✅ تنظیمات MVP بارگذاری شد!")
