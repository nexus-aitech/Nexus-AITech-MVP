from utils.logger import logger
from config import db

async def store_price_data(symbol, price, timestamp):
    try:
        price_collection = db["crypto_prices"]
        await price_collection.insert_one({
            "symbol": symbol.upper(),
            "price": price,
            "timestamp": timestamp
        })
        logger.info(f"✅ قیمت {symbol.upper()} = ${price} در {timestamp} ذخیره شد.")
    except Exception as e:
        logger.error(f"❌ خطا در ذخیره قیمت {symbol}: {e}")
