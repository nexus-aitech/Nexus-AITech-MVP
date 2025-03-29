# 📦 تصویر پایه رسمی TensorFlow با GPU پشتیبانی
FROM tensorflow/tensorflow:2.14.0-gpu

# 🛠️ تنظیم دایرکتوری کاری داخل کانتینر
WORKDIR /app

# 📁 کپی فایل‌های پروژه
COPY . /app

# 🧠 نصب پکیج‌ها (بدون کش و نسخه‌های وابسته)
RUN pip install --upgrade pip && \
    pip install --no-deps --ignore-installed -r requirements.txt

# ⚙️ تنظیمات محیطی برای پاک‌کردن .pyc و بدون بافر
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 🌐 پورت اجرای FastAPI یا Flask
EXPOSE 8080

# 🚀 اجرای API یا منطق مرکزی (main.py)
CMD ["python", "main.py"]

