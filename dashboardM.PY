import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import requests
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# API endpoint for fetching data from Core Coordinator
CORE_URL = "http://127.0.0.1:5000/api/process"

# Layout of the Dashboard
app.layout = dbc.Container([
    html.H1("📊 MVP Dashboard - Nexus-AITech", className="text-center text-light mb-4"),

    # Control Buttons
    dbc.Row([
        dbc.Col(html.Button("⏸ Pause Updates", id="pause-btn", n_clicks=0, className="btn btn-warning"), width=3),
        dbc.Col(dcc.Dropdown(
            id="time-range",
            options=[
                {"label": "Last 5 minutes", "value": "5min"},
                {"label": "Last 15 minutes", "value": "15min"},
                {"label": "Last 30 minutes", "value": "30min"},
                {"label": "Last 1 hour", "value": "1h"}
            ],
            value="5min",
            clearable=False,
            className="text-dark"
        ), width=4),
        dbc.Col(dcc.Checklist(
            id="data-filters",
            options=[
                {"label": " Show Cyber Security", "value": "cyber_defense"},
                {"label": " Show Blockchain", "value": "blockchain"},
                {"label": " Show Metaverse", "value": "metaverse"}
            ],
            value=["cyber_defense", "blockchain", "metaverse"],
            inline=True,
            className="text-light"
        ), width=5),
    ], className="mb-4"),

    # Dashboard Cards
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("🔐 Cyber Security"),
            dbc.CardBody([
                html.H4("Threats Detected:", className="card-title"),
                html.P("...", id='security-status', className="card-text"),
                dcc.Graph(id='security-chart')
            ])
        ], color="danger", outline=True), width=4),

        dbc.Col(dbc.Card([
            dbc.CardHeader("📊 Data Processing"),
            dbc.CardBody([
                html.H4("Analysis Summary:", className="card-title"),
                html.P("...", id='data-analysis', className="card-text"),
            ])
        ], color="primary", outline=True), width=4),

        dbc.Col(dbc.Card([
            dbc.CardHeader("💳 Fintech Transactions"),
            dbc.CardBody([
                html.H4("Transaction Status:", className="card-title"),
                html.P("...", id='fintech-status', className="card-text"),
                dcc.Graph(id='fintech-chart')
            ])
        ], color="success", outline=True), width=4),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("🌍 Metaverse Users"),
            dbc.CardBody([
                html.H4("Active Users:", className="card-title"),
                html.P("...", id='metaverse-users', className="card-text"),
                dcc.Graph(id='metaverse-chart')
            ])
        ], color="info", outline=True), width=6),

        dbc.Col(dbc.Card([
            dbc.CardHeader("⛓️ Blockchain Status"),
            dbc.CardBody([
                html.H4("Latest Block:", className="card-title"),
                html.P("...", id='blockchain-status', className="card-text"),
                dcc.Graph(id='blockchain-chart')
            ])
        ], color="warning", outline=True), width=6),
    ], className="mb-4"),

    dcc.Interval(
        id='interval-component',
        interval=5000,  # Updates every 5 seconds
        n_intervals=0
    )
], fluid=True)

# Function to fetch data from Core Coordinator
def fetch_data(bot_name):
    response = requests.post(CORE_URL, json={"bot_name": bot_name})
    if response.status_code == 200:
        return response.json().get("response", {})
    return {}

# Callback for updating the dashboard
@app.callback(
    [Output('security-status', 'children'),
     Output('security-chart', 'figure'),
     Output('data-analysis', 'children'),
     Output('fintech-status', 'children'),
     Output('fintech-chart', 'figure'),
     Output('metaverse-users', 'children'),
     Output('metaverse-chart', 'figure'),
     Output('blockchain-status', 'children'),
     Output('blockchain-chart', 'figure')],
    [Input('interval-component', 'n_intervals')],
    [State('pause-btn', 'n_clicks'), State('data-filters', 'value')]
)
def update_dashboard(n_intervals, pause_clicks, filters):
    if pause_clicks % 2 == 1:  # If paused, don't update
        return dash.no_update

    security_data = fetch_data("cyber_defense") if "cyber_defense" in filters else {}
    data_analysis = fetch_data("data_analysis")
    fintech_data = fetch_data("fintech")
    metaverse_data = fetch_data("metaverse") if "metaverse" in filters else {}
    blockchain_data = fetch_data("blockchain") if "blockchain" in filters else {}

    security_chart = go.Figure(data=[go.Bar(
        x=["Cyber Threats"],
        y=[security_data.get('threats_detected', 0)],
        marker_color='red'
    )]) if "cyber_defense" in filters else go.Figure()

    fintech_chart = go.Figure(data=[go.Pie(
        labels=["Successful", "Failed"],
        values=[fintech_data.get('transaction_status') == 'Success', fintech_data.get('transaction_status') != 'Success'],
        hole=0.4
    )])

    metaverse_chart = go.Figure(data=[go.Indicator(
        mode="number+gauge",
        value=metaverse_data.get('active_users', 0),
        gauge={'axis': {'range': [0, 500]}}
    )]) if "metaverse" in filters else go.Figure()

    blockchain_chart = go.Figure(data=[go.Scatter(
        x=["Blockchain"],
        y=[blockchain_data.get('latest_block', 0)],
        mode='markers',
        marker=dict(size=10, color="gold")
    )]) if "blockchain" in filters else go.Figure()

    return (
        f"Threats Detected: {security_data.get('threats_detected', 'N/A')}",
        security_chart,
        f"Analysis Summary: {data_analysis.get('summary', 'N/A')}",
        f"Transaction Status: {fintech_data.get('transaction_status', 'N/A')}, Amount: {fintech_data.get('amount', 'N/A')}",
        fintech_chart,
        f"Active Users: {metaverse_data.get('active_users', 'N/A')}",
        metaverse_chart,
        f"Latest Block: {blockchain_data.get('latest_block', 'N/A')}",
        blockchain_chart
    )

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
