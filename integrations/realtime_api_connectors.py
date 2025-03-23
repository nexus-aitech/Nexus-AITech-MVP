import aiohttp
import os

# ==== Fintech: KuCoin ====
async def get_kucoin_price(symbol="ETH-USDC"):
    url = f"https://api.kucoin.com/api/v1/market/stats?symbol={symbol}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return {
                "symbol": symbol,
                "price": data.get("data", {}).get("last")
            }

# ==== Blockchain: ANKR ====
async def get_latest_blockchain_data():
    ankr_url = "https://rpc.ankr.com/multichain"
    headers = {"Content-Type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 1
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(ankr_url, json=payload, headers=headers) as resp:
            result = await resp.json()
            return {"latest_block_hex": result.get("result")}

# ==== CoinMarketCap ====
async def get_coinmarketcap_price(symbol="SOL_USDC"):
    url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={symbol}"
    headers = {"X-CMC_PRO_API_KEY": os.getenv("COINMARKETCAP_API_KEY")}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            return {
                "symbol": symbol,
                "price": data.get("data", {}).get(symbol, {}).get("quote", {}).get("USD", {}).get("price")
            }

# ==== BingX Price ====
async def get_bingx_price(symbol="ARB-USDC"):
    url = f"https://open-api.bingx.com/openApi/swap/v2/quote/price?symbol={symbol}"
    headers = {"X-BX-APIKEY": os.getenv("BINGX_API_KEY")}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            return {"symbol": symbol, "price": data.get("price")}

# ==== Bitget ====
async def get_bitget_price(symbol="AVAX_USDC"):
    url = f"https://api.bitget.com/api/spot/v1/market/ticker?symbol={symbol}"
    headers = {"ACCESS-KEY": os.getenv("BITGET_API_KEY")}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            return {"symbol": symbol, "price": data.get("data", {}).get("last")}
