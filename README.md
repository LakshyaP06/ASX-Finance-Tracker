# ASX-Finance-Tracker
Top ASXs based on growth and stability tracker.

## Overview
The ASX Finance Tracker is an innovative application designed to aid users in identifying optimal ASX investments. This repository includes two complementary tools:

### 1. Growth & Stability Analysis Dashboard (Python/Streamlit)
Leveraging data scraped from Yahoo Finance, this application analyzes and evaluates ASX stocks based on two key variables: five-year growth potential and overall stability. The results are visually represented through interactive graphs, offering clear insights into performance trends. As the first prototype, the application showcases a preliminary algorithm for ranking ASX stocks, with planned enhancements to improve accuracy and reliability in future iterations. Additionally, the application includes a feature that enables users to download the analysis as a .csv file, providing a convenient way to access and utilize the tabulated results offline.

**Location:** `AsxFinanceTracker/` directory  
**Run:** `cd AsxFinanceTracker && streamlit run main.py`

### 2. Target Price Tracker (HTML/JavaScript)
A standalone HTML/JavaScript web application that compares current stock prices with analyst target prices from TradingView. This tool helps identify stocks with the highest upside potential by calculating the percentage difference between current and target prices, and displays analyst coverage for each stock.

**Location:** `stock-tracker.html`  
**Run:** Open `stock-tracker.html` in any web browser

## Features

### Target Price Tracker Features
- **Real-time Comparison:** Compare current prices vs. analyst target prices
- **Percentage Calculation:** Automatic calculation of upside/downside potential (e.g., LOT: current $0.21, target $0.30 = +42.86%)
- **Analyst Coverage:** Display number of analysts providing recommendations for each stock
- **Confidence Rating:** Visual indicators based on analyst count (High/Medium/Low)
- **Interactive Filtering:**
  - Search by ticker or company name
  - Filter by minimum analyst count (5+, 10+, 15+)
  - Filter by minimum upside percentage (20%+, 50%+, 100%+)
- **Sortable Columns:** Click any column header to sort ascending/descending
- **Summary Statistics:** 
  - Total stocks tracked
  - Average upside percentage
  - Best opportunity (highest % gain potential)
  - Highest analyst coverage
- **Responsive Design:** Works on desktop, tablet, and mobile devices

## Getting Started

### Target Price Tracker
Simply open `stock-tracker.html` in any modern web browser. No installation or dependencies required!

**Note:** The tracker currently displays sample data for demonstration. To use real TradingView data, you would need to:
- Set up a backend server to scrape TradingView (client-side scraping is blocked by CORS)
- Use TradingView's official API (requires paid subscription)
- Or manually update the stock data in the JavaScript section

### Growth & Stability Dashboard
1. Navigate to the `AsxFinanceTracker/` directory
2. Install dependencies: `pip install -r requirements.txt` or use the provided `pyproject.toml`
3. Run the application: `streamlit run main.py`

## Screenshots

### Target Price Tracker
![ASX Stock Tracker](https://github.com/user-attachments/assets/4e97d80b-eced-4330-bb7f-ebec50d1602a)

## Data Sources
- **Growth & Stability Dashboard:** Yahoo Finance
- **Target Price Tracker:** TradingView (sample data included for demonstration)

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
