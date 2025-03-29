import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import os
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

# ✅ لود متغیرهای محیطی
load_dotenv()
COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY")

app = FastAPI()

# ✅ تنظیم CORS برای دسترسی کلاینت‌ها
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ دریافت قیمت‌های ارز دیجیتال با `retry`
def fetch_crypto_prices(retries=3):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    symbols = ["ETH", "BNB", "SOL", "ADA", "DOT", "AVAX", "ARB"]
    params = {"symbol": ",".join(symbols), "convert": "USD"}
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY
    }

    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=5)
            response.raise_for_status()
            data = response.json().get("data", {})
            return {
                symbol: round(data.get(symbol, {}).get("quote", {}).get("USD", {}).get("price", 0), 2)
                for symbol in symbols
            }
        except requests.exceptions.RequestException as e:
            print(f"❌ خطا در دریافت قیمت ارزها: {e} (تلاش {attempt + 1})")
            if attempt < retries - 1:
                asyncio.sleep(2)  # ⬅️ اینو باید `await` کنیم
    return {symbol: None for symbol in symbols}

# ✅ دریافت داده‌های بلاکچین
async def fetch_transactions_from_network():
    return {
        "block_number": 17832234,
        "transactions": 5000,
        "analyzed": {"summary": "AI Analysis Complete"}
    }

# ✅ WebSocket
@app.websocket("/ws/live-data")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ WebSocket Client Connected!")  # 🛠 برای دیباگ

    try:
        while True:
            # ✅ گرفتن قیمت‌ها
            prices = fetch_crypto_prices()
            
            # ✅ گرفتن داده‌های بلاکچین
            block_analysis = await fetch_transactions_from_network()

            # ✅ ساختار داده‌های ارسالی
            data = {
                "timestamp": datetime.utcnow().isoformat(),
                "prices": prices,
                "blockchain": {
                    "ETH": 17832234,
                    "BNB": 33551221,
                    "SOL": 208320948,
                    "ADA": 123320,
                    "DOT": 827311,
                    "AVAX": 221037,
                    "ARB": 665101
                },
                "ai_teacher": {
                    "sessions_today": 12,
                    "learning_index": 0.89,
                    "students_active": 17
                },
                "data_analysis": {
                    "datasets_processed": 103,
                    "anomalies_detected": 2
                },
                "cyber_defense": {
                    "threats_detected": 5,
                    "ips_blocked": 2
                },
                "metaverse": {
                    "users_online": 48,
                    "events_today": 23
                },
                "core_coordinator": {
                    "bots_running": 6,
                    "system_health": "✅ Stable"
                },
                "block_analysis": {
                    "block_number": block_analysis.get("block_number"),
                    "transactions": block_analysis.get("transactions"),
                    "analyzed": block_analysis.get("analyzed")
                }
            }

            # ✅ ارسال داده‌ها به WebSocket
            print("📡 Sending WebSocket Data...")  # 🛠 برای دیباگ
            await websocket.send_text(json.dumps(data))
            await asyncio.sleep(10)

    except WebSocketDisconnect:
        print("❌ کلاینت قطع شد.")
    except Exception as e:
        print(f"❌ خطای عمومی در WebSocket: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
