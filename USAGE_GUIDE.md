# ASX Stock Tracker - Usage Guide

## Quick Start

### Opening the Tracker
1. Simply open `stock-tracker.html` in any modern web browser (Chrome, Firefox, Safari, Edge)
2. No installation or server setup required!

## Features Guide

### Understanding the Display

#### Statistics Dashboard
At the top of the page, you'll see four key metrics:
- **Total Stocks**: Number of stocks currently being tracked
- **Average Upside**: Mean percentage gain potential across all stocks
- **Best Opportunity**: Stock with the highest upside percentage
- **Highest Analyst Coverage**: Stock with the most analyst recommendations

#### Main Table Columns
1. **#** - Ranking number
2. **Ticker** - ASX stock ticker symbol
3. **Company** - Full company name
4. **Current Price** - Current trading price
5. **Target Price** - Analyst consensus target price
6. **% Upside/Downside** - Calculated percentage difference (green = positive, red = negative)
7. **Analyst Count** - Number of analysts providing recommendations
8. **Confidence** - Rating based on analyst count (High: 15+, Medium: 8-14, Low: <8)

### Using Filters

#### Search Function
- Type in the search box to filter by ticker or company name
- Example: Type "LOT" to see only Lotus Resources
- Example: Type "Bank" to see all banking stocks

#### Analyst Count Filter
Use the dropdown to show only stocks with sufficient analyst coverage:
- **All Analyst Counts**: Shows all stocks
- **5+ Analysts**: Stocks with at least 5 analysts
- **10+ Analysts**: Stocks with at least 10 analysts
- **15+ Analysts**: Stocks with at least 15 analysts (highest confidence)

#### Upside Filter
Use the dropdown to filter by minimum potential gain:
- **All Upside %**: Shows all stocks
- **20%+ Upside**: Only stocks with 20% or more upside
- **50%+ Upside**: Only stocks with 50% or more upside
- **100%+ Upside**: Only stocks with 100% or more upside

### Sorting Data
- Click any column header to sort by that column
- First click: Sort descending (highest to lowest)
- Second click: Sort ascending (lowest to highest)
- The arrow indicator shows current sort direction (↑ or ↓)

### Interpreting the Data

#### Percentage Calculation
The upside/downside is calculated as:
```
Upside % = ((Target Price - Current Price) / Current Price) × 100
```

**Example: LOT Stock**
- Current Price: $0.21
- Target Price: $0.30
- Calculation: (($0.30 - $0.21) / $0.21) × 100 = +42.86%

#### Confidence Ratings
- **High (Green)**: 15+ analysts - Strong consensus, higher reliability
- **Medium (Yellow)**: 8-14 analysts - Moderate coverage
- **Low (Red)**: <8 analysts - Limited coverage, higher uncertainty

#### Why Analyst Count Matters
More analysts providing recommendations generally indicates:
- Greater market interest in the stock
- More comprehensive research coverage
- Higher likelihood that the target is realistic
- Reduced impact of individual analyst bias

## Example Use Cases

### Finding High-Confidence Opportunities
1. Set "15+ Analysts" filter
2. Set "20%+ Upside" filter
3. Sort by "% Upside/Downside" (descending)
4. Review top stocks with strong analyst backing

### Researching a Specific Stock
1. Type the ticker (e.g., "BHP") in the search box
2. View its target price, upside, and analyst count
3. Compare against similar companies

### Discovering Hidden Gems
1. Set "50%+ Upside" filter
2. Sort by "Analyst Count" to find high-upside stocks with decent coverage
3. Research further before investing

## Important Notes

### Current Implementation
- The tracker displays **sample data** for demonstration
- Data is static and does not auto-refresh
- Real TradingView integration requires backend implementation

### Data Limitations
- Sample data represents realistic ASX stock structure
- Actual prices, targets, and analyst counts should be verified through official sources
- Always conduct your own research before making investment decisions

### Future Enhancements
To use real TradingView data, you would need to:
1. **Backend Server**: Set up a server to scrape TradingView (client-side is blocked by CORS)
2. **TradingView API**: Subscribe to TradingView's official API service
3. **Manual Updates**: Periodically update the stock data array in the JavaScript code

## Customization

### Adding New Stocks
1. Open `stock-tracker.html` in a text editor
2. Find the `sampleStocks` array (around line 270)
3. Add new stocks following this format:
```javascript
{ ticker: 'XXX', company: 'Company Name', currentPrice: 10.50, targetPrice: 12.00, analysts: 10 }
```

### Modifying Filters
You can adjust filter thresholds in the HTML:
- Find the `<select id="filterAnalysts">` section
- Add or modify `<option>` values

### Styling
All CSS is embedded in the `<style>` section - modify colors, fonts, and layout as needed.

## Troubleshooting

### Page Not Loading
- Ensure JavaScript is enabled in your browser
- Try a different browser (Chrome/Firefox recommended)
- Check browser console for errors (F12 → Console)

### No Data Showing
- Wait 1-2 seconds for initial load animation
- Click the "🔄 Refresh Data" button
- Clear browser cache and reload

### Filters Not Working
- Clear the search box first
- Reset filters to "All" options
- Refresh the page

## Support
For issues or questions, please open an issue on the GitHub repository.
