import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd

# Load cleaned data
df = pd.read_csv("processed_sales_data.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Soul Foods Sales Visualizer", style={"textAlign": "center"}),

    dcc.Graph(
        figure=go.Figure(
            data=[
                go.Scatter(
                    x=df["date"],
                    y=df["sales"],
                    mode="lines+markers",
                    name="Sales"
                )
            ],
            layout=go.Layout(
                title="Pink Morsel Sales Over Time",
                title_x=0.5,
                xaxis_title="Date",
                yaxis_title="Sales ($)",
                shapes=[{
                    "type": "line",
                    "x0": "2021-01-15",
                    "x1": "2021-01-15",
                    "y0": df["sales"].min(),
                    "y1": df["sales"].max(),
                    "line": {"color": "red", "width": 2, "dash": "dash"}
                }]
            )
        )
    )
])

if __name__ == "__main__":
    app.run(debug=True)

