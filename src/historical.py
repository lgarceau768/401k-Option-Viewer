import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import logging
import os
from datetime import datetime, timedelta

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
        # Calculate the start and end dates
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

        # Download historical data from Yahoo Finance
        stock_data = yf.download(symbol, start=start_date, end=end_date)

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

# Save the result to a new CSV file
result_df.to_csv('./out/historical_performance_yahoo_finance.csv', index=False)

# Create bar charts for each duration
for duration in ['1 Month', '3 Month', '6 Month', '1 Year']:
    # Create a bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(result_df['Investment Name'], result_df[f'{duration} Performance'], color='skyblue')
    plt.title(f'{duration} Performance of Investment Options 📊')
    plt.xlabel('Investment Name 🏦')
    plt.ylabel('Performance 💹')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Add top 5 table
    top5_table = result_df.sort_values(by=f'{duration} Performance', ascending=False).head(5)
    plt.table(cellText=top5_table[[f'{duration} Performance']].values,
              rowLabels=top5_table['Investment Name'],
              colLabels=[f'Top 5 in {duration}'],
              loc='bottom', cellLoc='center', colLoc='center', bbox=[0, -0.2, 1, 0.15])

    plt.savefig(f'./out/performance_chart_{duration.lower()}_yahoo_finance.png')
    plt.close()

# Create a bar chart for each stock's performance over 1, 3, 6, and 12 months
fig = go.Figure()

for duration in ['1 Month', '3 Month', '6 Month', '1 Year']:
    result_df_sorted = result_df.sort_values(by=f'{duration} Performance', ascending=True)
    rounded_performance = result_df_sorted[f'{duration} Performance'].round(5)

    # Create a bar trace for each duration
    trace = go.Bar(
        x=result_df_sorted['Symbol'],
        y=rounded_performance,
        text=result_df_sorted['Investment Name'],
        hoverinfo='text+y',
        name=f'{duration} Performance'
    )
    fig.add_trace(trace)

# Configure the layout
fig.update_layout(
    barmode='group',
    title='Stock Performance Over Time',
    xaxis_title='Stock Symbol',
    yaxis_title='Performance',
    showlegend=True
)

# Add click event handler to display selected stock's performance near the legend
fig.update_layout(
    updatemenus=[
        {
            'type': 'buttons',
            'showactive': False,
            'buttons': [
                {
                    'label': '1 Month',
                    'method': 'update',
                    'args': [{'visible': [True, False, False, False]}, {'title': '1 Month Performance'}]
                },
                {
                    'label': '3 Month',
                    'method': 'update',
                    'args': [{'visible': [False, True, False, False]}, {'title': '3 Month Performance'}]
                },
                {
                    'label': '6 Month',
                    'method': 'update',
                    'args': [{'visible': [False, False, True, False]}, {'title': '6 Month Performance'}]
                },
                {
                    'label': '1 Year',
                    'method': 'update',
                    'args': [{'visible': [False, False, False, True]}, {'title': '1 Year Performance'}]
                },
            ],
        },
    ]
)

# Save the chart as an HTML file
chart_file_path = './out/stock_performance_over_time.html'
fig.write_html(chart_file_path)

# Display the chart
fig.show()
