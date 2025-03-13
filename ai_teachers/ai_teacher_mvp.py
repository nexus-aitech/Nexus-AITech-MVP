import requests
import random

# آدرس سرور مرکزی (Core Coordinator)
CORE_URL = "http://localhost:5000/api/process"

# لیست دروس تستی
lessons = [
    "🔹 درس ۱: مقدمه‌ای بر هوش مصنوعی",
    "🔹 درس ۲: یادگیری ماشین چیست؟",
    "🔹 درس ۳: پردازش زبان طبیعی (NLP)",
    "🔹 درس ۴: شبکه‌های عصبی عمیق (Deep Learning)",
    "🔹 درس ۵: کاربردهای AI در فین‌تک"
]

def teach_lesson():
    """ شبیه‌سازی آموزش یک درس توسط معلم هوشمند """
    print("🎓 معلم هوشمند در حال ارائه درس...")

    # انتخاب یک درس تصادفی
    selected_lesson = random.choice(lessons)
    students_online = random.randint(5, 50)

    ai_teacher_data = {
        "lesson": selected_lesson,
        "students_online": students_online
    }

    print(f"📚 ارائه‌ی درس: {selected_lesson}")
    print(f"👩‍🎓 تعداد دانش‌آموزان آنلاین: {students_online}")

    # ارسال درخواست به Core Coordinator
    response = requests.post(CORE_URL, json={"bot_name": "ai_teacher"})
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ پاسخ Core Coordinator: {data['response']}")
    else:
        print("❌ خطا در دریافت پاسخ از Core Coordinator!")

if __name__ == "__main__":
    teach_lesson()

# Ai Teacher Mvp
print('Executing ai_teacher_mvp.py')
