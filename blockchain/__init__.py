from blockchain.blockchain_mvp import blockchain_mvp
print("✅ Blockchain Module Loaded!")

#   Init  
print('Executing __init__.py')

# اضافه کردن بررسی مسیر برای ایمپورت صحیح ماژول‌ها
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))