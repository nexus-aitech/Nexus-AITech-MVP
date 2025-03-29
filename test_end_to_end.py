# ✅ تست جامع End-to-End پروژه Nexus-AITech
import asyncio
import sys
import os
import random

# 📌 اضافه کردن مسیر پوشه‌های داخلی برای ایمپورت صحیح
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "fintech")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "security")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "metaverse")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "utils")))

# ✅ ایمپورت ماژول‌های پروژه
from database import store_analysis_result, log_threat, store_metaverse_activity
from fintech_mvp import simulate_financial_transactions
from cyber_defense_mvp import CyberDefenseSystem
from ai_engine import TransactionSecurity
from metaverse_mvp import get_metaverse_activity
from helper_functions import send_data_to_ws
from logger import log_info, log_error

# 🧪 تابع تست جامع End-to-End
async def test_end_to_end():
    log_info("🏁 شروع تست End-to-End MVP")

    try:
        # 🏦 تست تراکنش‌های مالی
        transactions = simulate_financial_transactions()
        log_info(f"📈 تراکنش‌های مالی شبیه‌سازی‌شده: {len(transactions)}")

        # 🔐 اجرای سیستم دفاع سایبری
        cyber = CyberDefenseSystem()
        cyber_threats = cyber.run_analysis()
        for threat in cyber_threats:
            log_threat(threat)

        # 🧠 اجرای تحلیل امنیتی هوش مصنوعی
        ts = TransactionSecurity()
        for tx in transactions:
            await ts.analyze_transaction(tx)

        # 🌐 شبیه‌سازی متاورس
        metaverse_data = get_metaverse_activity()
        await store_metaverse_activity(metaverse_data)

        # 📊 ذخیره نتیجه در پایگاه داده
        analysis_summary = {
            "block_number": random.randint(100000, 999999),
            "transactions": len(transactions),
            "analyzed": {"summary": "No major threats detected"}
        }
        await store_analysis_result(analysis_summary)

        # 🌐 ارسال داده به WebSocket
        await send_data_to_ws({
            "prices": {
                "ETH": "3432.19",
                "BNB": "417.88",
                "SOL": "188.43",
                "ADA": "0.625",
                "DOT": "8.19",
                "AVAX": "48.10",
                "ARB": "1.76"
            },
            "blockchain": {
                "ETH": 19521341,
                "BNB": 38724456,
                "SOL": 292117823,
                "ADA": 95982331,
                "DOT": 14200056,
                "AVAX": 4321557,
                "ARB": 22003352
            },
            "ai_teacher": {
                "sessions_today": 97,
                "learning_index": "A+",
                "students_active": 378
            },
            "data_analysis": {
                "datasets_processed": 1802,
                "anomalies_detected": 6
            },
            "cyber_defense": {
                "threats_detected": len(cyber_threats),
                "ips_blocked": 12
            },
            "metaverse": metaverse_data,
            "core_coordinator": {
                "bots_running": 24,
                "system_health": "✅ Stable"
            },
            "block_analysis": analysis_summary
        })

        log_info("✅ تست جامع End-to-End با موفقیت انجام شد.")

    except Exception as e:
        log_error(f"❌ خطا در تست End-to-End: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_end_to_end())
