# eBay Tech Deals Scraping and Analysis

## Project Overview
This project scrapes eBay Global Tech Deals, automates data collection via GitHub Actions, cleans the data, and performs exploratory data analysis.

## Methodology

### Task 1: Web Scraping
The scraper uses Selenium to navigate to eBay's tech deals page, scrolls to load all products via lazy loading, and extracts product information including timestamp, title, price, original price, shipping details, and product URLs.

### Task 2: Automation
GitHub Actions workflow runs every 3 hours (cron: `0 */3 * * *`) to automatically update the dataset. The workflow runs for approximately two days to build a comprehensive dataset before cleaning and analysis.

### Task 3: Data Cleaning
The cleaning script processes raw CSV data by:
- Removing currency symbols and formatting from price fields
- Handling missing original prices by replacing with current price
- Standardizing shipping information
- Calculating discount percentages

### Task 4: Exploratory Data Analysis
The Jupyter notebook performs comprehensive analysis including:
- Time series analysis of deals by hour
- Price distribution visualizations
- Discount analysis
- Shipping option frequency
- Keyword frequency in product titles
- Top discount identification

## Key Findings
Analysis reveals patterns in deal timing, price distributions, discount ranges, shipping preferences, and popular product categories.

## Challenges Faced
- Handling dynamic content loading on eBay's website
- Managing missing data in price fields
- Configuring GitHub Actions for automated scraping
- Dealing with varying HTML structures for product listings

## Potential Improvements
- Implement retry logic for failed scraping attempts
- Add data validation checks
- Expand keyword analysis with more categories
- Implement real-time alerting for high-value deals
- Add time-based trend analysis

## Files
- `scraper.py`: Web scraping script using Selenium
- `clean_data.py`: Data cleaning and processing script
- `EDA.ipynb`: Jupyter notebook with exploratory data analysis
- `.github/workflows/scrape.yml`: GitHub Actions workflow configuration
- `ebay_tech_deals.csv`: Raw scraped data
- `cleaned_ebay_deals.csv`: Processed and cleaned data

