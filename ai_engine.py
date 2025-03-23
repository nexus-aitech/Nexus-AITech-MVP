import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pickle
import os
from dotenv import load_dotenv
import logging
import pymongo
from datetime import datetime
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from market_api import get_live_crypto_price

# بارگذاری متغیرهای محیطی
load_dotenv()

# تنظیمات لاگ‌گیری
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AI Engine")

# اتصال به پایگاه داده MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = pymongo.MongoClient(MONGO_URI)
db = client["ai_teacher_db"]
blocks_collection = db["block_data"]

class DataAnalyzer:
    def __init__(self):
        print("✅ DataAnalyzer مقداردهی شد.")

    async def analyze(self, data):
        """متد تحلیل داده"""
        print("📊 تحلیل داده آغاز شد...")
        await asyncio.sleep(2)  # شبیه‌سازی پردازش داده
        print("📊 تحلیل داده کامل شد.")
        return {"result": "تحلیل کامل شد"}

    def train_model(self, data):
        """آموزش مدل تحلیل داده‌ها"""
        df = pd.DataFrame(data)
        X = self.scaler.fit_transform(df.drop(columns=["target"]))
    def predict_users(self, X_input):
        """پیش‌بینی تعداد کاربران آینده بر اساس داده‌های ورودی"""
        if not self.is_trained:
            raise ValueError("🚨 مدل هنوز آموزش ندیده است! لطفاً ابتدا متد train را اجرا کنید.")
        return self.model.predict(X_input)

        y = df["target"].values
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        self.is_trained = True
        logger.info("✅ مدل تحلیل داده‌ها آموزش داده شد.")

    def analyze_data(self, input_data):
        """تحلیل یک داده برای شناسایی الگوها"""
        if not self.is_trained:
            raise ValueError("🚨 مدل آموزش ندیده است! لطفاً ابتدا مدل را آموزش دهید.")
        
        input_df = pd.DataFrame([input_data])
        input_scaled = self.scaler.transform(input_df)
        prediction = self.model.predict(input_scaled)
        return prediction

class CyberThreatAnalyzer:
    """تحلیل تهدیدات سایبری و حملات سایبری"""
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False

    def train_model(self, security_data):
        """آموزش مدل تحلیل تهدیدات سایبری"""
        df = pd.DataFrame(security_data)
        df["threat_label"] = df["threat_label"].map({"safe": 0, "threat": 1})
        X = self.scaler.fit_transform(df.drop(columns=["threat_label"]))
        y = df["threat_label"].values
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        self.is_trained = True
        logger.info("✅ مدل تحلیل تهدیدات سایبری آموزش داده شد.")

    def analyze_threat(self, log_data):
        """تحلیل یک داده‌ی لاگ برای شناسایی تهدید سایبری"""
        if not self.is_trained:
            raise ValueError("🚨 مدل آموزش ندیده است! لطفاً ابتدا مدل را آموزش دهید.")
        
        log_df = pd.DataFrame([log_data])
        log_scaled = self.scaler.transform(log_df)
        prediction = self.model.predict(log_scaled)
        return "تهدید سایبری" if prediction[0] == 1 else "ایمن"

class FraudDetection:
    """مدل یادگیری ماشین برای شناسایی تراکنش‌های مشکوک و تقلبی"""
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False

    def train_model(self, transactions_data):
        """آموزش مدل برای شناسایی تقلب"""
        df = pd.DataFrame(transactions_data)
        df["label"] = df["label"].map({"legit": 0, "fraud": 1})
        X = self.scaler.fit_transform(df.drop(columns=["label"]))
        y = df["label"].values
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        self.is_trained = True
        logger.info("✅ مدل تشخیص تقلب آموزش داده شد.")

    def detect_fraud(self, transaction):
        """بررسی یک تراکنش برای شناسایی تقلب"""
        if not self.is_trained:
            raise ValueError("🚨 مدل آموزش ندیده است! لطفاً ابتدا مدل را آموزش دهید.")
        
        transaction_df = pd.DataFrame([transaction])
        transaction_scaled = self.scaler.transform(transaction_df)
        prediction = self.model.predict(transaction_scaled)
        return "تقلب" if prediction[0] == 1 else "عادی"

class DeepLearningPredictor:
    """
    یک مدل یادگیری عمیق برای پیش‌بینی‌های مختلف.
    """
    def __init__(self, input_shape=10):
        self.model = Sequential([
            Dense(64, activation="relu", input_shape=(input_shape,)),
            Dropout(0.2),
            Dense(32, activation="relu"),
            Dense(1, activation="sigmoid")
        ])
        self.model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
        self.is_trained = False

    def train(self, X_train, y_train, epochs=10, batch_size=32):
        """ آموزش مدل با داده‌های آموزشی """
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)
        self.is_trained = True
        logger.info("✅ مدل یادگیری عمیق آموزش داده شد.")

    def predict(self, X_test):
        """ پیش‌بینی خروجی با مدل آموزش‌دیده """
        if not self.is_trained:
            raise ValueError("🚨 مدل آموزش ندیده است! لطفاً ابتدا مدل را آموزش دهید.")
        return self.model.predict(X_test)

class AIRecommendationModel:
    """ مدل پیشنهاددهی هوشمند برای توصیه‌ی دروس به دانش‌آموزان """
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        self.is_trained = False

    def train_model(self, data):
        """ آموزش مدل پیشنهاددهی """
        df = pd.DataFrame(data)
        if "student_id" in df.columns:
            df = df.drop(columns=["student_id"])  
        df["recommended_subject"] = self.label_encoder.fit_transform(df["recommended_subject"])
        X = self.scaler.fit_transform(df.drop(columns=["recommended_subject"]))
        y = df["recommended_subject"].values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        self.is_trained = True
        logger.info("✅ مدل پیشنهاددهی آموزش داده شد.")

    def predict_subject(self, student_data):
        """ پیش‌بینی بهترین درس برای دانش‌آموز """
        if not self.is_trained:
            raise ValueError("🚨 مدل آموزش ندیده است! لطفاً ابتدا مدل را آموزش دهید.")
        student_df = pd.DataFrame([student_data])
        student_scaled = self.scaler.transform(student_df)
        prediction = self.model.predict(student_scaled)
        return self.label_encoder.inverse_transform(prediction)[0]

class TransactionAnalyzer:
    """ تحلیل تراکنش‌های بلاکچینی و مالی برای شناسایی الگوهای مشکوک """
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False

    def train_model(self, transactions_data):
        """ آموزش مدل تحلیل تراکنش‌ها """
        df = pd.DataFrame(transactions_data)
        df["label"] = df["label"].map({"legit": 0, "fraud": 1})
        X = self.scaler.fit_transform(df.drop(columns=["label"]))
        y = df["label"].values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        self.is_trained = True
        logger.info("✅ مدل تحلیل تراکنش‌ها آموزش داده شد.")

    def analyze_transaction(self, transaction):
        """ تحلیل یک تراکنش برای شناسایی فعالیت‌های مشکوک """
        if not self.is_trained:
            raise ValueError("🚨 مدل آموزش ندیده است! لطفاً ابتدا مدل را آموزش دهید.")
        transaction_df = pd.DataFrame([transaction])
        transaction_scaled = self.scaler.transform(transaction_df)
        prediction = self.model.predict(transaction_scaled)
        return "مشکوک" if prediction[0] == 1 else "عادی"

class TransactionSecurity:
    """ بررسی امنیت تراکنش‌ها با استفاده از الگوریتم‌های یادگیری ماشین """
    def __init__(self):
        self.security_model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False

    def train_security_model(self, security_data):
        """ آموزش مدل امنیتی برای تشخیص تراکنش‌های غیرمجاز """
        df = pd.DataFrame(security_data)
        df["security_label"] = df["security_label"].map({"safe": 0, "threat": 1})
        X = self.scaler.fit_transform(df.drop(columns=["security_label"]))
        y = df["security_label"].values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.security_model.fit(X_train, y_train)
        self.is_trained = True
        logger.info("✅ مدل امنیتی آموزش داده شد.")

    def check_security_risk(self, transaction):
        """ بررسی امنیت یک تراکنش """
        if not self.is_trained:
            raise ValueError("🚨 مدل امنیتی آموزش ندیده است! لطفاً ابتدا مدل را آموزش دهید.")
        transaction_df = pd.DataFrame([transaction])
        transaction_scaled = self.scaler.transform(transaction_df)
        prediction = self.security_model.predict(transaction_scaled)
        return "خطر امنیتی" if prediction[0] == 1 else "ایمن"

def store_block_data(block):
    """ذخیره اطلاعات بلاک‌های بلاکچین در پایگاه داده"""
    try:
        block["timestamp"] = datetime.utcnow()
        blocks_collection.insert_one(block)
        logger.info(f"✅ بلاک با شناسه {block.get('block_hash')} در پایگاه داده ذخیره شد.")
    except Exception as e:
        logger.error(f"❌ خطا در ذخیره بلاک: {e}")

class CryptoPredictor:
    """مدل یادگیری ماشین برای پیش‌بینی قیمت ارزهای دیجیتال"""
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False

    def train_model(self, market_data):
        """آموزش مدل با داده‌های بازار"""
        df = pd.DataFrame(market_data)
        df["target"] = df["target"].astype(float)
        X = self.scaler.fit_transform(df.drop(columns=["target"]))
        y = df["target"].values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        self.is_trained = True
        logger.info("✅ مدل CryptoPredictor آموزش داده شد.")

    def predict_price(self, input_data):
        """پیش‌بینی قیمت آینده با استفاده از ویژگی‌های ورودی"""
        if not self.is_trained:
            raise ValueError("🚨 مدل آموزش ندیده است! لطفاً ابتدا متد train_model را اجرا کنید.")
        input_df = pd.DataFrame([input_data])
        input_scaled = self.scaler.transform(input_df)
        prediction = self.model.predict(input_scaled)
        return prediction[0]

if __name__ == "__main__":
    sample_block = {"block_hash": "abc123", "transactions": 15, "miner": "0xMinerAddress"}
    store_block_data(sample_block)

# اصلاح لیست `__all__`
__all__ = ["AIRecommendationModel", "TransactionAnalyzer", "TransactionSecurity", "DeepLearningPredictor", "FraudDetection", "store_block_data", "CryptoPredictor", "get_live_crypto_price"]
