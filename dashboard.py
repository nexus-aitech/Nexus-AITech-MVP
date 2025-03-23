import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import requests
from flask import Flask, jsonify
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from config import ACTIVE_BOTS
from blockchain_live import get_latest_block  # دریافت لیست بات‌ها از config.py

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

CORE_URL = "http://127.0.0.1:5000/api/process"

# داینامیک کردن لیست بات‌ها
bot_options = [{"label": f" Show {bot.replace('_', ' ').title()}", "value": bot} for bot in ACTIVE_BOTS]

@app.server.route("/api/data")
def get_dashboard_data():
    """API برای دریافت داده‌های داشبورد"""
    data = {}
    for bot in ACTIVE_BOTS:
        data[bot] = fetch_data(bot)
    
    # افزودن داده‌های بلاکچین‌های مختلف به API
    data["blockchain"] = {
        "eth": get_latest_block("eth"),
        "bnb": get_latest_block("bnb"),
        "arb": get_latest_block("arb"),
        "avax": get_latest_block("avax"),
        "sol": get_latest_block("sol")
    }
    return jsonify(data)
    

def fetch_data(bot_name):
    """ دریافت داده‌های به‌روز از API داشبورد """
    try:
        response = requests.get("http://127.0.0.1:8050/api/data")
        if response.status_code == 200:
            data = response.json()
            return data.get(bot_name, {})  # دریافت داده مخصوص این بات
    except requests.exceptions.RequestException:
        print(f"⚠️ خطا در دریافت داده‌های {bot_name}")
    return {}

    

    app.run_server(debug=True, port=8050)


app.layout = dbc.Container([
    html.H2("📡 Real-Time Blockchain Monitor", className="text-center my-4"),
    dcc.Graph(id="live-blocks"),
    dcc.Interval(id="interval-update", interval=10000, n_intervals=0)
])

@app.callback(
    Output("live-blocks", "figure"),
    [Input("interval-update", "n_intervals")]
)
def update_graph(n):
    try:
        response = requests.get("http://127.0.0.1:8050/api/data")
        if response.status_code == 200:
            data = response.json().get("blockchain", {})
            chains = []
            values = []
            for chain, info in data.items():
                if "block_number" in info:
                    chains.append(chain.upper())
                    values.append(info["block_number"])
                elif "block_height" in info:
                    chains.append(chain.upper())
                    values.append(info["block_height"])

            fig = go.Figure(data=[go.Bar(x=chains, y=values)])
            fig.update_layout(title="آخرین بلاک هر شبکه", yaxis_title="Block Number / Height")
            return fig
        else:
            return go.Figure()
    except Exception as e:
        return go.Figure()


if __name__ == '__main__':
    app.run_server(debug=True)