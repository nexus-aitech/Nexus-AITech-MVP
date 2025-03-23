#   Init  
print('Executing __init__.py')

# اضافه کردن بررسی مسیر برای ایمپورت صحیح ماژول‌ها
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

from .data_analysis_mvp import *
print("✅ Data Analysis Module Loaded!")