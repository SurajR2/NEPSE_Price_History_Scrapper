# NEPSE Price History Scrapper

This is a Python-based scraper to collect company data from Sharesansar, a stock market information website. The scraper fetches the company's recent data, including stock prices and historical data. It uses `Selenium` for web scraping and `BeautifulSoup` for parsing HTML.

### Features

This script allows you to scrape the following data for a company:

- **Current Stock Price**
- **Price Change**
- **Volume**
- **52-Week High and Low**
- **Open, High, Low Prices** (for the current market day)
- **Other Market Day Details**

Additionally, you can scrape **historical price data** for the company, up to 250 days before.

The data will be saved in CSV format for further analysis.

You can choose between scraping:

- **Recent Data** (current market day details)
- **Historical Price Data** (up to 250 days)

## Requirements

Before using this scraper, ensure you have the following Python packages installed:

- `selenium`# Hi there! this is the Nepse WebScraper
- `beautifulsoup4`
- `chromedriver_autoinstaller`
- `lxml`
- `re`
- `os`
- `csv`

To install the required libraries, run the following:

```bash
pip install > requirements.txt
```

# Company Data Scraper

## Usage

1. **Clone this repository:**

   ```bash
   git clone https://github.com/yourusername/CompanyDataScraper.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd CompanyDataScraper
   ```

3. **Run the scraper script:**

   ```bash
   python scraper.py
   ```

4. **Enter the company symbol** (e.g., 'anlb' for Aatmanirbhar Laghubitta Bittiya Sanstha Limited).

5. **Choose whether to scrape the recent data or price history** by answering the prompts (`y` for yes, `n` for no).

6. **The scraper will create a folder** for the company and save the data in CSV files:
   - `company_info.csv` – Contains the most recent stock data.
   - `price_history.csv` – Contains historical price data (if selected).

## How it Works

### 1. Initializing the Scraper

When the script is run, the scraper initializes a headless Chrome WebDriver using Selenium. It loads the company page based on the company symbol you provide.

### 2. Scraping Recent Data

It scrapes the company's name and various stock market data for the current day, such as:

- Current price
- Price change
- Open, high, low prices
- 52-week high-low
- Average prices for 120 and 180 days.

The data is saved in a CSV file with the date when the data was scraped.

### 3. Scraping Price History

If selected, the scraper clicks on the "Price History" section and collects historical data. It saves data from the price history table in a CSV file.

### 4. Saving the Data

The collected data is saved into two CSV files:

- `company_info.csv` – For the most recent company data.
- `price_history.csv` – For the historical data (if selected by the user).

Both files are saved in a folder named after the company in the current working directory.

## Example

Here is an example of the process:

```bash
Enter the company symbol: anlb
Do you want to scrape Recent Data? (y/n): y
Do you want to scrape Price History? (y/n): y
```

## Notes

- The script uses headless mode for Chrome, so no browser window will open during scraping.
- Ensure that `chromedriver_autoinstaller` installs the correct version of ChromeDriver based on your Chrome browser version.
- The script waits for some time (`time.sleep`) after each action to ensure the page is loaded completely before extracting data. You may need to adjust the timing based on your network speed.
- If the data extraction takes too long or there is an error, you may need to adjust the waiting times or ensure that your network connection is stable.

## Contributing

If you would like to contribute to this project, feel free to fork the repository, make changes, and submit a pull request. Here are a few ways you can help:

- Improve the scraping efficiency (e.g., handling large datasets).
- Add new features such as support for additional data points.
- Report any bugs or issues you find.

To submit changes, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Create a pull request to merge your changes into the main repository.

## License

This project is open-source and available under the MIT License.

### Author: `Suraj Rasaili BK`
