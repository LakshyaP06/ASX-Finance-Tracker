# TradingView Integration Guide

This document explains how to integrate real TradingView data into the stock tracker.

## Current Implementation

The tracker currently uses **sample data** defined in the JavaScript:

```javascript
const sampleStocks = [
    { ticker: 'LOT', company: 'Lotus Resources Limited', currentPrice: 0.21, targetPrice: 0.30, analysts: 8 },
    // ... more stocks
];
```

## Integration Options

### Option 1: Backend Server (Recommended)

Create a backend API to scrape TradingView data and serve it to the frontend.

#### Example: Python Flask Backend

**backend.py:**
```python
from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

@app.route('/api/stocks')
def get_stocks():
    stocks = []
    
    # Example: Scrape TradingView for each stock
    tickers = ['ASX:LOT', 'ASX:BHP', 'ASX:CBA']  # etc.
    
    for ticker in tickers:
        # This is a simplified example - actual implementation would need
        # to handle TradingView's dynamic content and anti-scraping measures
        url = f'https://www.tradingview.com/symbols/{ticker}/'
        
        # You would need to use Selenium or similar for dynamic content
        # This is just a structural example
        data = scrape_tradingview_data(ticker)
        
        if data:
            stocks.append({
                'ticker': data['ticker'],
                'company': data['company'],
                'currentPrice': data['current_price'],
                'targetPrice': data['target_price'],
                'analysts': data['analyst_count']
            })
    
    return jsonify(stocks)

def scrape_tradingview_data(ticker):
    # Implement actual scraping logic here
    # This would require handling:
    # 1. Authentication (if needed)
    # 2. JavaScript rendering (use Selenium)
    # 3. Rate limiting
    # 4. Error handling
    pass

if __name__ == '__main__':
    app.run(port=5000)
```

**Update stock-tracker.html:**
```javascript
// Replace the sampleStocks array loading with:
async function loadStockData() {
    const loadingArea = document.getElementById('loadingArea');
    loadingArea.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Loading stock data from TradingView...</p>
        </div>
    `;

    try {
        // Fetch from your backend API
        const response = await fetch('http://localhost:5000/api/stocks');
        const stocks = await response.json();
        
        // Process the data
        currentData = stocks.map(stock => ({
            ...stock,
            upside: parseFloat(calculateUpside(stock.currentPrice, stock.targetPrice)),
            confidence: getConfidenceLevel(stock.analysts)
        }));

        loadingArea.innerHTML = '';
        sortAndDisplayData();
        updateStats();
    } catch (error) {
        loadingArea.innerHTML = `
            <div class="error">
                <p>Error loading data: ${error.message}</p>
            </div>
        `;
    }
}
```

### Option 2: TradingView Official API

Subscribe to TradingView's paid API service.

**Update stock-tracker.html:**
```javascript
async function loadStockData() {
    const loadingArea = document.getElementById('loadingArea');
    loadingArea.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Loading stock data from TradingView API...</p>
        </div>
    `;

    try {
        // Replace with your TradingView API endpoint and credentials
        const API_KEY = 'your_api_key_here';
        const response = await fetch('https://api.tradingview.com/v1/data', {
            headers: {
                'Authorization': `Bearer ${API_KEY}`
            }
        });
        
        const data = await response.json();
        
        // Transform API response to match our data structure
        currentData = data.stocks.map(stock => ({
            ticker: stock.symbol.replace('ASX:', ''),
            company: stock.name,
            currentPrice: stock.price,
            targetPrice: stock.analyst_target,
            analysts: stock.analyst_count,
            upside: parseFloat(calculateUpside(stock.price, stock.analyst_target)),
            confidence: getConfidenceLevel(stock.analyst_count)
        }));

        loadingArea.innerHTML = '';
        sortAndDisplayData();
        updateStats();
    } catch (error) {
        loadingArea.innerHTML = `
            <div class="error">
                <p>Error loading data: ${error.message}</p>
            </div>
        `;
    }
}
```

### Option 3: Manual Data Updates

Manually update the stock data periodically.

1. Visit TradingView for each stock
2. Note down: current price, target price, analyst count
3. Update the `sampleStocks` array in `stock-tracker.html`
4. Save and refresh

**Example:**
```javascript
const sampleStocks = [
    // Updated 2024-10-01
    { ticker: 'LOT', company: 'Lotus Resources Limited', currentPrice: 0.21, targetPrice: 0.30, analysts: 8 },
    { ticker: 'BHP', company: 'BHP Group Limited', currentPrice: 43.50, targetPrice: 52.00, analysts: 22 },
    // ... update other stocks
];
```

## Web Scraping Best Practices

If implementing Option 1 (backend scraping):

### 1. Respect Robots.txt
```python
from urllib.robotparser import RobotFileParser

rp = RobotFileParser()
rp.set_url("https://www.tradingview.com/robots.txt")
rp.read()

if rp.can_fetch("*", url):
    # Proceed with scraping
    pass
```

### 2. Implement Rate Limiting
```python
import time

def scrape_with_delay(url, delay=2):
    time.sleep(delay)  # Wait between requests
    return requests.get(url)
```

### 3. Use Proper Headers
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}
response = requests.get(url, headers=headers)
```

### 4. Handle Dynamic Content
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get(url)

# Wait for dynamic content to load
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "price")))

current_price = element.text
```

### 5. Implement Error Handling
```python
def safe_scrape(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return None
```

## Caching Strategy

To reduce API calls and improve performance:

```javascript
// Cache data for 1 hour
const CACHE_DURATION = 60 * 60 * 1000; // 1 hour in milliseconds

async function loadStockData() {
    const cached = localStorage.getItem('stockData');
    const cacheTime = localStorage.getItem('stockDataTime');
    
    // Use cached data if it's fresh
    if (cached && cacheTime) {
        const age = Date.now() - parseInt(cacheTime);
        if (age < CACHE_DURATION) {
            currentData = JSON.parse(cached);
            sortAndDisplayData();
            updateStats();
            return;
        }
    }
    
    // Fetch fresh data
    try {
        const response = await fetch('http://localhost:5000/api/stocks');
        const stocks = await response.json();
        
        // Cache the data
        localStorage.setItem('stockData', JSON.stringify(stocks));
        localStorage.setItem('stockDataTime', Date.now().toString());
        
        // Process and display
        currentData = stocks;
        sortAndDisplayData();
        updateStats();
    } catch (error) {
        console.error('Error loading data:', error);
    }
}
```

## Legal Considerations

⚠️ **Important:** 
- Always check TradingView's Terms of Service before scraping
- Consider using official APIs when available
- Respect rate limits and robots.txt
- Don't use scraped data for commercial purposes without permission
- Implement proper attribution if required

## Deployment

Once you have a working backend:

1. Deploy backend to a cloud service (Heroku, AWS, Google Cloud)
2. Update the API URL in stock-tracker.html
3. Ensure CORS is properly configured
4. Set up monitoring and error alerting
5. Implement API authentication if needed

## Testing

Create a test file to validate your integration:

**test_integration.js:**
```javascript
async function testDataFetch() {
    try {
        const response = await fetch('http://localhost:5000/api/stocks');
        const data = await response.json();
        
        console.log('✅ API accessible');
        console.log(`✅ Received ${data.length} stocks`);
        
        // Validate data structure
        const requiredFields = ['ticker', 'company', 'currentPrice', 'targetPrice', 'analysts'];
        const firstStock = data[0];
        
        requiredFields.forEach(field => {
            if (firstStock[field] !== undefined) {
                console.log(`✅ ${field} field present`);
            } else {
                console.error(`❌ ${field} field missing`);
            }
        });
        
        return true;
    } catch (error) {
        console.error('❌ Error:', error);
        return false;
    }
}

testDataFetch();
```

## Need Help?

For questions or issues with integration, please:
1. Check TradingView's documentation
2. Review the Flask/Django documentation for backend setup
3. Open an issue on the GitHub repository
