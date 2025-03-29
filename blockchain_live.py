import asyncio
import requests
import os
import logging
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# تنظیمات لاگ‌گیری
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("BlockchainLive")

# دریافت API Keyها از .env
ALCHEMY_ETH_MAINNET = os.getenv("ALCHEMY_ETH_MAINNET")
ALCHEMY_AVAX_MAINNET = os.getenv("ALCHEMY_AVAX_MAINNET")
ALCHEMY_ARB_MAINNET = os.getenv("ALCHEMY_ARB_MAINNET")
ALCHEMY_BNB_MAINNET = os.getenv("ALCHEMY_BNB_MAINNET")
ALCHEMY_SOLANA_MAINNET = os.getenv("ALCHEMY_SOLANA_MAINNET")

CHAINSTACK_SOLANA_MAINNET = os.getenv("CHAINSTACK_SOLANA_MAINNET")
QUIKNODE_BSC_MAINNET = os.getenv("QUIKNODE_BSC_MAINNET")
INFURA_ARB_MAINNET = os.getenv("INFURA_ARB_MAINNET")
ANKR_API_KEY = os.getenv("ANKR_API_KEY")

# دیکشنری آدرس API بلاکچین‌ها
BLOCKCHAIN_APIS = {
    "eth": ALCHEMY_ETH_MAINNET,
    "avax": ALCHEMY_AVAX_MAINNET,
    "arbitrum": ALCHEMY_ARB_MAINNET,
    "bnb": ALCHEMY_BNB_MAINNET,
    "solana": CHAINSTACK_SOLANA_MAINNET or ALCHEMY_SOLANA_MAINNET,
}

def get_latest_block(chain="eth"):
    """دریافت آخرین بلاک از شبکه انتخابی"""
    try:
        url = BLOCKCHAIN_APIS.get(chain)
        if not url:
            logger.error(f"❌ شبکه '{chain}' پشتیبانی نمی‌شود یا URL یافت نشد.")
            return {"error": "Unsupported or missing chain URL"}

        # انتخاب روش مناسب برای درخواست
        if chain == "solana":
            payload = {"jsonrpc": "2.0", "id": 1, "method": "getBlockHeight", "params": None}
        else:  # برای Ethereum و سایر شبکه‌های EVM
            payload = {"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1}
        
        # ارسال درخواست
        response = requests.post(url, json=payload, timeout=8)
        response.raise_for_status()
        result = response.json()

        # پردازش خروجی
        if chain == "solana":
            return {"block_height": result.get("result")}
        else:
            block_hex = result.get("result")
            if block_hex:
                return {"block_number": int(block_hex, 16)}

        return {"error": "⚠️ No result from blockchain"}

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ خطا در درخواست API: {e}")
        return {"error": f"API request failed: {str(e)}"}

# تست مستقیم فایل
if __name__ == "__main__":
    for chain in BLOCKCHAIN_APIS.keys():
        status = get_latest_block(chain)
        print(f"{chain.upper()} Latest Block:", status)
