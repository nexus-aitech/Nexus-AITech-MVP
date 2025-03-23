
import requests

ANKR_API_KEYS = {
    "eth": "https://rpc.ankr.com/eth/218f85885f390b202fd7857edbd458a21e0523862d396b40ce937e4074a9d6cc",
    "bnb": "https://rpc.ankr.com/bsc/218f85885f390b202fd7857edbd458a21e0523862d396b40ce937e4074a9d6cc",
    "arb": "https://rpc.ankr.com/arbitrum/218f85885f390b202fd7857edbd458a21e0523862d396b40ce937e4074a9d6cc",
    "avax": "https://rpc.ankr.com/avalanche/218f85885f390b202fd7857edbd458a21e0523862d396b40ce937e4074a9d6cc",
    "sol": "https://rpc.ankr.com/solana/218f85885f390b202fd7857edbd458a21e0523862d396b40ce937e4074a9d6cc"
}

def get_latest_block(chain="eth"):
    try:
        url = ANKR_API_KEYS.get(chain)
        if not url:
            return {"error": "Unsupported chain"}

        if chain == "sol":
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getBlockHeight",
                "params": None
            }
        else:
            payload = {
                "jsonrpc": "2.0",
                "method": "eth_blockNumber",
                "params": [],
                "id": 1
            }

        response = requests.post(url, json=payload)
        result = response.json()
        
        if chain == "sol":
            height = result.get("result")
            return {"block_height": height}
        else:
            block_hex = result.get("result")
            if block_hex:
                return {"block_number": int(block_hex, 16)}
        
        return {"error": "Invalid response"}
    except Exception as e:
        return {"error": str(e)}

def get_balance(chain="eth", address="0x0000000000000000000000000000000000000000"):
    try:
        url = ANKR_API_KEYS.get(chain)
        if not url or chain == "sol":
            return {"error": "Unsupported chain for balance"}

        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getBalance",
            "params": [address, "latest"],
            "id": 1
        }

        response = requests.post(url, json=payload)
        result = response.json()
        balance_hex = result.get("result")
        if balance_hex:
            balance_eth = int(balance_hex, 16) / 10**18
            return {"balance": balance_eth}
        else:
            return {"error": "Invalid response"}
    except Exception as e:
        return {"error": str(e)}
