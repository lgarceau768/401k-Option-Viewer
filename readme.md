# Retirement Options Viewer
Author: Luke Garceau
This project fetches historical performance data for different investment options using the Yahoo Finance API and visualizes the data through interactive charts. The performance is measured over 1 month, 3 months, 6 months, and 1 year periods.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Install required Python packages using the provided `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### Usage

Run the script to fetch historical performance data and generate visualizations:

```bash
python3 scr/historical.py
```

## Directory Structure

```
.
├── data
│   └── symbol_mapping.csv
├── logs
│   └── historical_performance.log
├── out
│   ├── historical_performance_yahoo_finance.csv
│   ├── performance_chart_1_month_yahoo_finance.png
│   ├── performance_chart_3_month_yahoo_finance.png
│   ├── performance_chart_6_month_yahoo_finance.png
│   ├── performance_chart_1_year_yahoo_finance.png
│   ├── stock_performance_over_time.html
│   └── top5_table_{duration}_yahoo_finance.html
├── script.py
└── requirements.txt
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- [Yahoo Finance API](https://rapidapi.com/apidojo/api/yahoo-finance1)
