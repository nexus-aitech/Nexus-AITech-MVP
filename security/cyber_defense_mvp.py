import asyncio
import random
import sys
import os
import json
import requests
from datetime import datetime
from utils.logger import log_info, log_error
from ai_engine import CyberThreatAnalyzer
from database import log_threat, block_ip
from utils.fake_data_provider import FakeDataProvider  # ✅ استفاده از داده‌ساز فیک

# اضافه کردن مسیر پروژه برای اطمینان از ایمپورت صحیح ماژول‌ها
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

# آدرس سرور مرکزی
CORE_URL = os.getenv("CORE_URL", "http://localhost:8080/api/process")

class CyberDefenseSystem:
    """سیستم امنیت سایبری برای شناسایی تهدیدات"""
    def __init__(self):
        log_info("\ud83d\udee1\ufe0f CyberDefenseSystem مقداردهی شد.")
        self.analyzer = CyberThreatAnalyzer()

    async def scan_network(self):
        """ استفاده از داده فیک برای شبیه‌سازی تحلیل امنیتی """
        log_info("\ud83d\udd0d شبیه‌سازی اسکن امنیتی شبکه با داده‌های واقع‌گرایانه...")
        await asyncio.sleep(1)
        fake_data = FakeDataProvider.generate_cyber_threats()
        threats = []
        for threat_type in fake_data.get("threat_types", []):
            threats.append({
                "source_ip": f"192.168.{random.randint(1,255)}.{random.randint(1,255)}",
                "severity": "HIGH" if random.random() > 0.5 else "LOW",
                "description": f"Detected threat: {threat_type}"
            })
        return threats

async def detect_threats(self):
    """شناسایی تهدیدات سایبری و اعمال اقدامات لازم"""
    log_info("در حال شناسایی تهدیدات سایبری...")  # حذف ایموجی که باعث کرش می‌شد
    threats_detected = await self.scan_network()

    if threats_detected:
        for threat in threats_detected:
            await log_threat(threat)
            if threat['severity'] == "HIGH":
                await block_ip(threat['source_ip'])
                log_info(f"تهدید خطرناک شناسایی شد و آی‌پی مسدود شد: {threat['source_ip']}")

    try:
        response = requests.post(CORE_URL, json={"bot_name": "cyber_defense", "threats": threats_detected}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            log_info(f"✅ گزارش امنیتی از سرور مرکزی دریافت شد: {data.get('response', 'No response data')}")
        else:
            log_error(f"❌ خطا در دریافت گزارش امنیتی! وضعیت HTTP: {response.status_code}")
    except requests.exceptions.ConnectionError:
        log_error("ارتباط با Core Coordinator امکان‌پذیر نیست! سیستم مستقل عمل می‌کند...")
    except requests.exceptions.Timeout:
        log_error("⏳ درخواست به Core Coordinator تایم‌اوت شد. تحلیل محلی ادامه دارد.")
    except Exception as e:
        log_error(f"⚠️ خطای غیرمنتظره: {e}")

async def run_cyber_defense():
    """ اجرای مداوم سیستم امنیت سایبری """
    cyber_defense = CyberDefenseSystem()
    while True:
        await cyber_defense.detect_threats()
        await asyncio.sleep(10)

async def detect_threats():
    """
    نسخه مستقل تابع برای ایمپورت مستقیم از بیرون
    """
    system = CyberDefenseSystem()
    await system.detect_threats()

if __name__ == "__main__":
    log_info("\ud83d\ude80 Cyber Defense System در حال راه‌اندازی...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_cyber_defense())