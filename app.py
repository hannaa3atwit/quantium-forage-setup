import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# ---------- Load & prep data ----------
df = pd.read_csv("output.csv")

# If your output file used lowercase headers from the earlier task,
# this normalizes them so the app still works.
df.columns = [c.strip().lower() for c in df.columns]

# Expect: sales, date, region
df["date"] = pd.to_datetime(df["date"])
df["region"] = df["region"].str.lower()
df = df.sort_values("date")

PRICE_INCREASE_DATE = pd.to_datetime("2021-01-15")

def build_figure(region_value: str):
    """Return a line chart filtered by region and aggregated by date."""
    working = df.copy()

    if region_value != "all":
        working = working[working["region"] == region_value]

    # total sales per day (for the selected region or all regions)
    daily = working.groupby("date", as_index=False)["sales"].sum()

    fig = px.line(daily, x="date", y="sales", markers=True)

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales",
        margin=dict(l=40, r=20, t=40, b=40),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    # Price increase reference line
    fig.add_vline(
        x=PRICE_INCREASE_DATE,
        line_dash="dash",
        annotation_text="Price Increase (2021-01-15)",
        annotation_position="top left",
    )

    # Light gridlines
    fig.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.08)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.08)")

    return fig


# ---------- Dash app ----------
app = Dash(__name__)
app.title = "Pink Morsels Sales Visualiser"

# Simple styling (inline CSS)
PAGE_STYLE = {
    "fontFamily": "Arial, sans-serif",
    "background": "linear-gradient(135deg, #f6f9ff 0%, #fdf7ff 100%)",
    "minHeight": "100vh",
    "padding": "24px",
}

CARD_STYLE = {
    "maxWidth": "980px",
    "margin": "0 auto",
    "backgroundColor": "white",
    "borderRadius": "16px",
    "padding": "22px",
    "boxShadow": "0 10px 30px rgba(0, 0, 0, 0.08)",
    "border": "1px solid rgba(0,0,0,0.06)",
}

TITLE_STYLE = {
    "margin": "0 0 6px 0",
    "fontSize": "28px",
    "fontWeight": "700",
    "color": "#1f2937",
}

SUBTITLE_STYLE = {
    "margin": "0 0 18px 0",
    "color": "#4b5563",
    "lineHeight": "1.4",
}

CONTROL_ROW_STYLE = {
    "display": "flex",
    "gap": "16px",
    "alignItems": "center",
    "flexWrap": "wrap",
    "padding": "14px",
    "borderRadius": "12px",
    "backgroundColor": "#f8fafc",
    "border": "1px solid rgba(0,0,0,0.06)",
    "marginBottom": "14px",
}

LABEL_STYLE = {
    "fontWeight": "700",
    "color": "#111827",
}

RADIO_CONTAINER_STYLE = {
    "display": "flex",
    "gap": "14px",
    "alignItems": "center",
    "flexWrap": "wrap",
}

app.layout = html.Div(
    style=PAGE_STYLE,
    children=[
        html.Div(
            style=CARD_STYLE,
            children=[
                html.H1("Soul Foods Pink Morsels Sales Visualiser", style=TITLE_STYLE),
                html.P(
                    "Question: Were sales higher before or after the Pink Morsel price increase on Jan 15, 2021? "
                    "Use the region filter to dig into local trends.",
                    style=SUBTITLE_STYLE,
                ),

                html.Div(
                    style=CONTROL_ROW_STYLE,
                    children=[
                        html.Span("Filter by region:", style=LABEL_STYLE),
                        dcc.RadioItems(
                            id="region-filter",
                            options=[
                                {"label": "All", "value": "all"},
                                {"label": "North", "value": "north"},
                                {"label": "East", "value": "east"},
                                {"label": "South", "value": "south"},
                                {"label": "West", "value": "west"},
                            ],
                            value="all",
                            labelStyle={"display": "inline-block", "cursor": "pointer"},
                            inputStyle={"marginRight": "6px"},
                            style=RADIO_CONTAINER_STYLE,
                        ),
                    ],
                ),

                dcc.Graph(
                    id="sales-line-chart",
                    figure=build_figure("all"),
                    config={"displayModeBar": False},
                    style={"height": "520px"},
                ),

                html.Div(
                    style={
                        "marginTop": "10px",
                        "fontSize": "12px",
                        "color": "#6b7280",
                        "textAlign": "right",
                    },
                    children="Data source: Soul Foods transaction CSVs (Pink Morsels only)",
                ),
            ],
        )
    ],
)

# ---------- Callback (radio -> chart update) ----------
@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value"),
)
def update_chart(region_value):
    return build_figure(region_value)


if __name__ == "__main__":
    app.run_server(debug=True)
