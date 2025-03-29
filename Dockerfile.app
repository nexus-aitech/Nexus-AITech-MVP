# 📦 تصویر پایه رسمی TensorFlow با GPU پشتیبانی
FROM tensorflow/tensorflow:2.14.0-gpu

# 🛠️ تنظیم دایرکتوری کاری داخل کانتینر
WORKDIR /app

# 📁 کپی فایل‌های پروژه
COPY . /app

# 🛠️ نصب ابزارهای موردنیاز
RUN apt-get update && apt-get install -y python3 python3-venv python3-pip

# 🧠 ایجاد و فعال‌سازی venv و نصب وابستگی‌ها
RUN python3 -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# ⚙️ تنظیمات محیطی برای بدون بافر و بدون ایجاد .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"

# 🌐 پورت اجرای FastAPI یا Flask
EXPOSE 8080

# 🚀 اجرای API یا منطق مرکزی (main.py)
CMD ["python", "main.py"]
