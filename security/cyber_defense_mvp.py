import asyncio
import os
import json
import requests
from datetime import datetime
from utils.logger import log_info, log_error
from ai_engine import CyberThreatAnalyzer
from database import log_threat, block_ip

# اضافه کردن مسیر پروژه برای اطمینان از ایمپورت صحیح ماژول‌ها
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

# آدرس سرور مرکزی
CORE_URL = os.getenv("CORE_URL", "http://localhost:5000/api/process")

class CyberDefenseSystem:
    """سیستم امنیت سایبری برای شناسایی تهدیدات"""
    def __init__(self):
        log_info("🛡️ CyberDefenseSystem مقداردهی شد.")
        self.analyzer = CyberThreatAnalyzer()

    async def scan_network(self):
        """ اسکن شبکه برای شناسایی تهدیدات سایبری """
        log_info("🔍 اسکن امنیتی شبکه در حال اجراست...")
        await asyncio.sleep(3)  # شبیه‌سازی تحلیل امنیتی
        return [{
            "source_ip": "192.168.1.1",
            "severity": "HIGH",
            "description": "Malicious traffic detected"
        }]

    async def detect_threats(self):
        """شناسایی تهدیدات سایبری و اعمال اقدامات لازم"""
        log_info("🔍 در حال شناسایی تهدیدات سایبری...")
        threats_detected = await self.scan_network()

        if threats_detected:
            for threat in threats_detected:
                await log_threat(threat, datetime.now())
                if threat['severity'] == "HIGH":
                    await block_ip(threat['source_ip'])  # بلاک کردن آی‌پی مهاجم
                    log_info(f"🚨 تهدید خطرناک شناسایی شد و آی‌پی مسدود شد: {threat['source_ip']}")
        
        try:
            response = requests.post(CORE_URL, json={"bot_name": "cyber_defense", "threats": threats_detected}, timeout=5)
            if response.status_code == 200:
                data = response.json()
                log_info(f"✅ گزارش امنیتی از سرور مرکزی دریافت شد: {data.get('response', 'No response data')}")
            else:
                log_error(f"❌ خطا در دریافت گزارش امنیتی! وضعیت HTTP: {response.status_code}")
        except requests.exceptions.ConnectionError:
            log_error("🚨 ارتباط با Core Coordinator امکان‌پذیر نیست! سیستم مستقل عمل می‌کند...")
        except requests.exceptions.Timeout:
            log_error("⏳ درخواست به Core Coordinator تایم‌اوت شد. تحلیل محلی ادامه دارد.")
        except Exception as e:
            log_error(f"⚠️ خطای غیرمنتظره: {e}")

async def run_cyber_defense():
    """ اجرای مداوم سیستم امنیت سایبری """
    cyber_defense = CyberDefenseSystem()
    while True:
        await cyber_defense.detect_threats()
        await asyncio.sleep(10)  # اجرای نظارت زنده هر 10 ثانیه

async def detect_threats():
    """
    نسخه مستقل تابع برای ایمپورت مستقیم از بیرون
    """
    system = CyberDefenseSystem()
    await system.detect_threats()

if __name__ == "__main__":
    log_info("🚀 Cyber Defense System در حال راه‌اندازی...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_cyber_defense())