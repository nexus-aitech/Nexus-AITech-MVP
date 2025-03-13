import threading
import time
from config import MVP_CONFIG, ACTIVE_BOTS
from core import core_coordinator_mvp
from security import cyber_defense_mvp
from analytics import data_analysis_mvp
from fintech import fintech_mvp
from metaverse import metaverse_mvp
from ai_teachers import ai_teacher_mvp
from blockchain import blockchain_mvp

# لیست بات‌ها برای اجرا
BOTS = {
    "core_coordinator": core_coordinator_mvp.app.run,
    "cyber_defense": cyber_defense_mvp.detect_threats,
    "data_analysis": data_analysis_mvp.analyze_data,
    "fintech": fintech_mvp.process_transaction,
    "metaverse": metaverse_mvp.connect_to_metaverse,
    "ai_teacher": ai_teacher_mvp.teach_lesson,
    "blockchain": blockchain_mvp.check_blockchain_status,
}

def run_bot(bot_name):
    """اجرای هر بات در یک ترد جداگانه"""
    if bot_name in BOTS:
        print(f"🚀 راه‌اندازی {bot_name} ...")
        BOTS[bot_name]()
    else:
        print(f"⚠️ خطا: بات {bot_name} یافت نشد!")

def start_mvp():
    """اجرای تمام بات‌های فعال"""
    print("🔥 MVP در حال اجرا است ...")

    # اجرای Core Coordinator به‌صورت مستقل
    core_thread = threading.Thread(target=BOTS["core_coordinator"], kwargs={
        "host": MVP_CONFIG["HOST"],
        "port": MVP_CONFIG["PORT"],
        "debug": MVP_CONFIG["DEBUG"],
        "use_reloader": False
    })
    core_thread.start()
    time.sleep(2)  # صبر برای راه‌اندازی کامل Core Coordinator

    # اجرای سایر بات‌ها در تردهای جداگانه
    threads = []
    for bot_name in ACTIVE_BOTS:
        if bot_name != "core_coordinator":
            t = threading.Thread(target=run_bot, args=(bot_name,))
            threads.append(t)
            t.start()
            time.sleep(1)  # فاصله بین اجرای بات‌ها

    # انتظار برای پایان تمام تردها
    for t in threads:
        t.join()

    print("✅ MVP با موفقیت اجرا شد!")

if __name__ == "__main__":
    start_mvp()

# Main
print('Executing main.py')
