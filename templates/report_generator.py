# 🌐 Nexus-AITech Report Generator - HTML + PDF

import os
import pdfkit
from jinja2 import Environment, FileSystemLoader
from database import get_latest_analysis, get_latest_threats, get_latest_metaverse_data
from datetime import datetime
from logger import logger


def generate_html_report(output_path="report.html"):
    try:
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("report_template.html")

        # دریافت داده‌ها از MongoDB (یا mock در صورت نیاز)
        analysis_data = get_latest_analysis(limit=10)
        threats = get_latest_threats(limit=10)
        metaverse = get_latest_metaverse_data(limit=10)

        html_content = template.render(
            generated_at=datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
            analysis_data=analysis_data,
            threats=threats,
            metaverse=metaverse
        )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        logger.info("\u2705 گزارش HTML با موفقیت تولید شد")
        return output_path

    except Exception as e:
        logger.error(f"❌ خطا در تولید گزارش HTML: {e}")
        return None


def convert_html_to_pdf(html_path, pdf_path="report.pdf"):
    try:
        pdfkit.from_file(html_path, pdf_path)
        logger.info("\U0001F4C4 گزارش PDF با موفقیت تولید شد")
        return pdf_path
    except Exception as e:
        logger.error(f"❌ خطا در تبدیل به PDF: {e}")
        return None


if __name__ == "__main__":
    html_file = generate_html_report()
    if html_file:
        convert_html_to_pdf(html_file)