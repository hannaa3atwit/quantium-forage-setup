import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

# Load the formatted output from the previous task
df = pd.read_csv("output.csv")

# Ensure correct column names and types
# Expected columns: Sales, Date, Region
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# Optional: aggregate total sales per day across regions
daily_sales = df.groupby("Date", as_index=False)["Sales"].sum()

# Build the line chart
fig = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    title="Pink Morsels Sales Over Time"
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales",
)

# Add a reference line for the price increase date (Jan 15, 2021)
fig.add_vline(
    x=pd.to_datetime("2021-01-15"),
    line_dash="dash",
    annotation_text="Price Increase (2021-01-15)",
    annotation_position="top left"
)

app = Dash(__name__)

app.layout = html.Div(
    style={"fontFamily": "Arial", "padding": "20px"},
    children=[
        html.H1("Soul Foods Pink Morsels Sales Visualiser"),
        html.P(
            "Goal: Determine whether sales were higher before or after the Pink Morsel price increase on Jan 15, 2021."
        ),
        dcc.Graph(figure=fig),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
