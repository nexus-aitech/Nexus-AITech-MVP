import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import json
from dash_extensions import WebSocket
import dash_bootstrap_components as dbc

# ✅ راه‌اندازی اپ Dash با تم حرفه‌ای
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# ✅ Dashboard Layout
app.layout = dbc.Container([
    html.H1("🌍 Nexus-AITech | Live Data Dashboard", className="text-center text-light mb-4"),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("📊 Crypto Prices"),
            dbc.CardBody([
                html.P("ETH: ", className="fw-bold"), html.H4(id="eth-price", className="text-primary"),
                html.P("BNB: ", className="fw-bold"), html.H4(id="bnb-price", className="text-success"),
                html.P("SOL: ", className="fw-bold"), html.H4(id="sol-price", className="text-warning"),
                html.P("ADA: ", className="fw-bold"), html.H4(id="ada-price", className="text-danger"),
                html.P("DOT: ", className="fw-bold"), html.H4(id="dot-price", className="text-info"),
                html.P("AVAX: ", className="fw-bold"), html.H4(id="avax-price", className="text-secondary"),
                html.P("ARB: ", className="fw-bold"), html.H4(id="arb-price", className="text-muted"),
            ])
        ], color="dark", outline=True), width=4),

        dbc.Col(dbc.Card([
            dbc.CardHeader("🔗 Blockchain Status"),
            dbc.CardBody([
                dcc.Graph(id="blockchain-graph")
            ])
        ], color="dark", outline=True), width=8)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("🧑‍🏫 AI Teacher"),
            dbc.CardBody([
                html.P("📚 Sessions Today: ", className="fw-bold"), html.H4(id="ai-sessions", className="text-warning"),
                html.P("📊 Learning Index: ", className="fw-bold"), html.H4(id="ai-learning", className="text-info"),
                html.P("👥 Active Students: ", className="fw-bold"), html.H4(id="ai-students", className="text-success"),
            ])
        ], color="dark", outline=True), width=4),

        dbc.Col(dbc.Card([
            dbc.CardHeader("🛡️ Cybersecurity"),
            dbc.CardBody([
                html.P("🚨 Threats Detected: ", className="fw-bold"), html.H4(id="cyber-threats", className="text-danger"),
                html.P("🔒 Blocked IPs: ", className="fw-bold"), html.H4(id="cyber-blocked", className="text-warning"),
            ])
        ], color="dark", outline=True), width=4),

        dbc.Col(dbc.Card([
            dbc.CardHeader("🛠️ System Status"),
            dbc.CardBody([
                html.P("🤖 Bots Running: ", className="fw-bold"), html.H4(id="bots-running", className="text-success"),
                html.P("🟢 System Health: ", className="fw-bold"), html.H4(id="system-health", className="text-info"),
            ])
        ], color="dark", outline=True), width=4),
    ], className="mb-4"),

    # ✅ WebSocket Connection
    WebSocket(id="ws", url="ws://localhost:8000/ws/live-data")
], fluid=True)

@app.callback(
    [
        Output("eth-price", "children"),
        Output("bnb-price", "children"),
        Output("sol-price", "children"),
        Output("ada-price", "children"),
        Output("dot-price", "children"),
        Output("avax-price", "children"),
        Output("arb-price", "children"),
        Output("blockchain-graph", "figure"),
        Output("ai-sessions", "children"),
        Output("ai-learning", "children"),
        Output("ai-students", "children"),
        Output("cyber-threats", "children"),
        Output("cyber-blocked", "children"),
        Output("bots-running", "children"),
        Output("system-health", "children")
    ],
    [Input("ws", "message")]
)
def update_dashboard(message):
    """ پردازش داده‌های WebSocket و آپدیت داشبورد """
    print("📡 WebSocket Message Received:", message)

    try:
        if not message or "data" not in message:
            print("⚠️ WebSocket پیام نامعتبر دریافت کرد!")
            return ["-" for _ in range(7)] + [go.Figure()] + ["-" for _ in range(7)]

        # ✅ پردازش داده‌های دریافتی
        data = json.loads(message["data"]) if isinstance(message["data"], str) else message["data"]
        print("✅ WebSocket Data:", data)

        # ✅ استخراج داده‌ها
        prices = data.get("prices", {})
        blockchain = data.get("blockchain", {})
        ai_teacher = data.get("ai_teacher", {})
        cyber_defense = data.get("cyber_defense", {})
        core_coordinator = data.get("core_coordinator", {})

        # ✅ بررسی داده‌های بلاکچین قبل از رسم نمودار
        if not blockchain or not isinstance(blockchain, dict) or len(blockchain) == 0:
            print("⚠️ داده‌ای برای بلاکچین دریافت نشد، نمایش نمودار خالی")
            fig = go.Figure(layout={
                "title": "🔗 وضعیت بلاکچین (بدون داده)",
                "xaxis": {"title": "بلاک‌ها"},
                "yaxis": {"title": "تعداد"},
                "template": "plotly_dark"
            })
        else:
            # ✅ رسم نمودار با داده‌های معتبر
            fig = go.Figure(data=[
                go.Bar(x=list(blockchain.keys()), y=list(blockchain.values()), marker=dict(color='dodgerblue'))
            ])
            fig.update_layout(title="🔗 وضعیت بلاکچین", yaxis_title="تعداد بلاک‌ها", template="plotly_dark")

        return (
            f"${prices.get('ETH', '-')}",
            f"${prices.get('BNB', '-')}",
            f"${prices.get('SOL', '-')}",
            f"${prices.get('ADA', '-')}",
            f"${prices.get('DOT', '-')}",
            f"${prices.get('AVAX', '-')}",
            f"${prices.get('ARB', '-')}",
            fig,
            f"{ai_teacher.get('sessions_today', '-')} جلسه",
            f"{ai_teacher.get('learning_index', '-')} 📊",
            f"{ai_teacher.get('students_active', '-')} نفر",
            f"{cyber_defense.get('threats_detected', '-')} 🚨",
            f"{cyber_defense.get('ips_blocked', '-')} 🔒",
            f"{core_coordinator.get('bots_running', '-')} 🤖",
            core_coordinator.get("system_health", "❌ نامشخص")
        )

    except Exception as e:
        print(f"❌ خطا در پردازش WebSocket: {e}")
        return ["-" for _ in range(7)] + [go.Figure()] + ["-" for _ in range(7)]

# ✅ اجرای داشبورد
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=8050)

