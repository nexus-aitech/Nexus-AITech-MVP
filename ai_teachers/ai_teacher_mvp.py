import asyncio
import logging
import sys
import os
from typing import Dict, List
from datetime import datetime
from utils.logger import log_info, log_error

# اضافه کردن مسیر پروژه به sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

# تنظیم لاگر داخلی برای اطمینان از لاگ‌گیری
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class AIRecommendationModel:
    """مدل پیشنهادی هوش مصنوعی برای انتخاب درس مناسب"""
    def recommend_lesson(self, user_id: str) -> str:
        return f"Lesson for {user_id}"

class AITeacherSimulator:
    """شبیه‌ساز معلم هوشمند برای آموزش به دانش‌آموزان"""
    def __init__(self):
        self.ai_model = AIRecommendationModel()

    async def fetch_lesson(self, user_id: str) -> str:
        await asyncio.sleep(1)
        return self.ai_model.recommend_lesson(user_id)

    async def teach_lesson(self, students: List[str]) -> Dict[str, str]:
        if not students:
            log_info("🚫 هیچ دانش‌آموز فعالی برای تدریس وجود ندارد.")
            return {}
        
        log_info("📚 در حال ارائه درس به دانش‌آموزان...")
        tasks = {student: self.fetch_lesson(student) for student in students}
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        
        lesson_results = {}
        for student, result in zip(tasks.keys(), results):
            if isinstance(result, Exception):
                log_error(f"❌ خطا در تدریس به {student}: {result}")
                continue
            lesson_results[student] = result
            log_info(f"✅ درس برای {student} ارائه شد: {result}")
        
        return lesson_results

async def simulate_ai_teacher():
    """شبیه‌سازی معلم هوشمند"""
    log_info("📚 شبیه‌سازی معلم هوشمند در حال اجرا...")
    await asyncio.sleep(2)
    log_info("📚 شبیه‌سازی معلم هوشمند کامل شد.")

async def start_ai_teacher():
    """اجرای زنده معلم هوشمند با زمان‌بندی وظایف"""
    ai_teacher = AITeacherSimulator()
    try:
        while True:
            students = ["user1", "user2", "user3"]
            await ai_teacher.teach_lesson(students)
            await asyncio.sleep(10)
    except asyncio.CancelledError:
        log_info("🛑 اجرای معلم هوشمند متوقف شد.")

if __name__ == "__main__":
    log_info("🚀 AI Teacher در حال راه‌اندازی برای اجرای زنده...")
    try:
        asyncio.run(start_ai_teacher())
    except RuntimeError as e:
        log_error(f"❌ خطا در اجرای معلم هوشمند: {e}")