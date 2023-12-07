import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import logging
import os

# Create a logs directory if it doesn't exist
log_dir = './logs'
os.makedirs(log_dir, exist_ok=True)

# Configure logging
logging.basicConfig(filename=os.path.join(log_dir, 'historical_performance.log'), level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Read the symbol mapping CSV file into a DataFrame
symbol_mapping = pd.read_csv('./data/symbol_mapping.csv')

# Function to fetch historical performance data from Yahoo Finance
def fetch_historical_performance(row):
    investment_name = row['Investment Name']
    symbol = row['Symbol']

    # Emoji logging
    logging.info(f'🚀 Fetching data for {investment_name} ({symbol})...')

    try:
        # Download historical data from Yahoo Finance
        startDate = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        endDate = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        stock_data = yf.download(symbol, start='2022-01-01', end='2023-01-01')

        # Calculate performances
        performances = {
            '1 Month Performance': stock_data['Adj Close'].pct_change(periods=1).iloc[-1] * 100,
            '3 Month Performance': stock_data['Adj Close'].pct_change(periods=3).iloc[-1] * 100,
            '6 Month Performance': stock_data['Adj Close'].pct_change(periods=6).iloc[-1] * 100,
            '1 Year Performance': stock_data['Adj Close'].pct_change(periods=252).iloc[-1] * 100,
        }

        logging.info(f'✅ Data fetched successfully for {investment_name} ({symbol}).')
        return pd.Series({
            'Investment Name': investment_name,
            'Symbol': symbol,
            **performances,
        })
    except Exception as e:
        logging.error(f'❌ Unable to fetch data for {investment_name} ({symbol}). Error: {e}')
        return pd.Series({
            'Investment Name': investment_name,
            'Symbol': symbol,
            '1 Month Performance': None,
            '3 Month Performance': None,
            '6 Month Performance': None,
            '1 Year Performance': None,
        })

# Apply the function to each row of the symbol mapping DataFrame
result_df = symbol_mapping.apply(fetch_historical_performance, axis=1)

# Create Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1("Investment Performance Dashboard"),
    
    # Button for viewing the main chart
    html.Button("View Main Chart", id="view-main-chart", n_clicks=0),
    
    # Button for viewing top 5 table
    html.Button("View Top 5 Table", id="view-top5-table", n_clicks=0),

    # Output container
    html.Div(id='output-container'),

    # Graph component for displaying performance data
    dcc.Graph(id='performance-chart'),

    # Table component for displaying top 5 investments
    dcc.Graph(id='top5-table'),
])

# Define callback for button clicks
@app.callback(
    [Output('output-container', 'children'),
     Output('performance-chart', 'figure'),
     Output('top5-table', 'figure')],
    [Input('view-main-chart', 'n_clicks'),
     Input('view-top5-table', 'n_clicks')]
)
def update_page(main_chart_clicks, top5_table_clicks):
    ctx = dash.callback_context
    button_id = ctx.triggered_id if ctx.triggered_id else 'view-main-chart'

    if button_id == 'view-main-chart':
        # Update the page for the main chart view
        output = "Main Chart View"
        main_chart_fig = create_main_chart(result_df)
        top5_table_fig = None
    elif button_id == 'view-top5-table':
        # Update the page for the top 5 table view
        output = "Top 5 Table View"
        main_chart_fig = None
        top5_table_fig = create_top5_table(result_df, '1 Month Performance')
    else:
        # Initial page load
        output = ""
        main_chart_fig = None
        top5_table_fig = None

    return output, main_chart_fig, top5_table_fig

def create_main_chart(df):
    # Create a combined chart showing all 1, 3, 6, 12 month performances
    fig = go.Figure()

    for duration in ['1 Month', '3 Month', '6 Month', '1 Year']:
        fig.add_trace(go.Bar(
            x=df['Symbol'],
            y=df[f'{duration} Performance'],
            name=f'{duration} Performance',
            hoverinfo='y+name',
        ))

    fig.update_layout(
        barmode='group',
        title='Investment Performance Over Time',
        xaxis_title='Investment Symbol',
        yaxis_title='Performance (%)',
        showlegend=True,
    )

    return fig

def create_top5_table(df, duration_column):
    # Create a visual table for the top 5 investments
    top5_table = df.sort_values(by=duration_column, ascending=False).head(5)
    top5_table_fig = go.Figure(data=[go.Table(
        header=dict(values=['Investment Name', 'Symbol', f'{duration_column}']),
        cells=dict(values=[top5_table['Investment Name'], top5_table['Symbol'], top5_table[duration_column]]),
    )])

    top5_table_fig.update_layout(
        title=f'Top 5 Investments - {duration_column}',
    )

    return top5_table_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
