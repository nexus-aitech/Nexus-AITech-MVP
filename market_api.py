
import requests

# کلید API پروژه
COINMARKETCAP_API_KEY = "3ff1b233-f4ff-4342-848e-94970ae6f364"

def get_live_crypto_price(symbol="BTC"):
    """
    دریافت قیمت زنده از CoinMarketCap با API Key
    """
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    parameters = {
        "symbol": symbol.upper(),
        "convert": "USD"
    }
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY
    }

    try:
        response = requests.get(url, headers=headers, params=parameters)
        if response.status_code == 200:
            data = response.json()
            return round(data["data"][symbol.upper()]["quote"]["USD"]["price"], 2)
        else:
            print("خطا در دریافت قیمت:", response.status_code, response.text)
            return 0
    except Exception as e:
        print("خطای اتصال:", e)
        return 0
