import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load preprocessed sales data
df = pd.read_csv("processed_sales_data.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Soul Foods Visualizer"

# Available region filters
regions = ['all', 'north', 'south', 'east', 'west']

# Layout
app.layout = html.Div(style={
    'fontFamily': 'Arial, sans-serif',
    'backgroundColor': '#f4f4f4',
    'padding': '40px'
}, children=[
    html.H1("Soul Foods Sales Visualizer", style={
        'textAlign': 'center',
        'color': '#2c3e50'
    }),

    html.H3("Pink Morsel Sales Over Time", style={
        'textAlign': 'center',
        'color': '#34495e',
        'marginBottom': '30px'
    }),

    html.Div([
        html.Label("Filter by Region:", style={
            'fontWeight': 'bold',
            'marginRight': '20px',
            'color': '#2c3e50'
        }),
        dcc.RadioItems(
            id='region-filter',
            options=[{'label': region.capitalize(), 'value': region} for region in regions],
            value='all',
            labelStyle={'display': 'inline-block', 'marginRight': '20px'}
        )
    ], style={'textAlign': 'center', 'marginBottom': '40px'}),

    dcc.Graph(id='sales-chart'),

    html.Div(id='summary', style={
        'maxWidth': '700px',
        'margin': '50px auto 0',
        'padding': '20px',
        'backgroundColor': '#ffffff',
        'borderRadius': '10px',
        'boxShadow': '0px 2px 10px rgba(0,0,0,0.1)',
        'color': '#2c3e50'
    })
])


@app.callback(
    Output('sales-chart', 'figure'),
    Output('summary', 'children'),
    Input('region-filter', 'value')
)
def update_graph(region):
    filtered_df = df if region == 'all' else df[df['region'] == region]

    if filtered_df.empty:
        return go.Figure(), [html.H4("No data available for this selection.")]

    before = filtered_df[filtered_df['date'] < '2021-01-15']
    after = filtered_df[filtered_df['date'] >= '2021-01-15']
    avg_before = before['sales'].mean()
    avg_after = after['sales'].mean()

    figure = {
        'data': [
            go.Scatter(
                x=filtered_df['date'],
                y=filtered_df['sales'],
                mode='lines+markers',
                name='Sales',
                line=dict(color='#3498db', width=2),
                marker=dict(size=6),
                hovertemplate='<b>Date:</b> %{x}<br><b>Sales:</b> $%{y:.2f}<extra></extra>'
            ),
            go.Scatter(
                x=[filtered_df['date'].min(), filtered_df['date'].max()],
                y=[avg_before, avg_before],
                mode='lines',
                name='Avg Before 15 Jan 2021',
                line=dict(color='green', width=2, dash='dash')
            ),
            go.Scatter(
                x=[filtered_df['date'].min(), filtered_df['date'].max()],
                y=[avg_after, avg_after],
                mode='lines',
                name='Avg After 15 Jan 2021',
                line=dict(color='red', width=2, dash='dot')
            )
        ],
        'layout': go.Layout(
            title=f'Sales in {region.capitalize()} Region' if region != 'all' else 'Sales in All Regions',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Sales ($)'),
            plot_bgcolor='white',
            paper_bgcolor='white',
            hovermode='closest',
            shapes=[
                dict(
                    type='line',
                    x0='2021-01-15',
                    x1='2021-01-15',
                    y0=0,
                    y1=1,
                    yref='paper',
                    line=dict(color='red', width=2, dash='dash')
                )
            ],
            annotations=[
                dict(
                    x='2021-01-15',
                    y=1.05,
                    xref='x',
                    yref='paper',
                    showarrow=False,
                    text='Price Increase',
                    font=dict(color='red'),
                    align='center'
                )
            ]
        )
    }

    summary_text = [
        html.H4("Sales Summary"),
        html.P(f"Average sales before price increase: ${avg_before:.2f}"),
        html.P(f"Average sales after price increase: ${avg_after:.2f}"),
        html.P("Sales dropped after price increase." if avg_after < avg_before else "Sales increased after price increase.")
    ]

    return figure, summary_text


if __name__ == '__main__':
    app.run(debug=True)
