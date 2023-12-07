# Retirement Options Viewer
Author: Luke Garceau
Date: 2023-12-07
This project fetches historical performance data for investment options using the Yahoo Finance API.

## Usage

1. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Run the script:

    ```bash
    python3 src/historical.py
    ```

## Outputs

- Historical performance data: [historical_performance_alpha_vantage.csv](./output/historical_performance_alpha_vantage.csv)
- Performance charts:
  - [1 Month Performance Chart](./output/performance_chart_1_month.png)
  - [3 Month Performance Chart](./output/performance_chart_3_month.png)
  - [6 Month Performance Chart](./output/performance_chart_6_month.png)
  - [1 Year Performance Chart](./output/performance_chart_1_year.png)
- Top 5 Investments for 1 Month Performance: [top5_investments.md](./output/top5_investments.md)
- [Log directory](./output/)

### Requirements.txt

