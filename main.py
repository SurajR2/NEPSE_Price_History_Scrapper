import re
import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from bs4 import BeautifulSoup
import chromedriver_autoinstaller


class CompanyDataScraper:
    def __init__(self, company_symbol):
        # Generate the URL based on the company symbol
        self.company_url = f'https://www.sharesansar.com/company/{company_symbol}'
        self.company_symbol = company_symbol
        self.driver = self._initialize_driver()

    def _initialize_driver(self):
        # Installing Chrome Driver
        path = chromedriver_autoinstaller.install()

        # Set chrome options to enable headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("window-size=1200,800")

        # Launch Chrome in headless mode
        service = Service(path)
        return webdriver.Chrome(service=service, options=chrome_options)

    def scrape_company_data(self, scrape_recent_data=True, scrape_price_history=True):
        self.driver.get(self.company_url)
        time.sleep(3)  # Wait for the page to load

        # Get the page source after the interaction
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        
        ###extracting company name and removing newline and unnecessary whitesapce that might be present###
        company_name_tag = soup.find('h1')
        company_name = company_name_tag.get_text(separator=" ", strip=True).replace("\n", " ")
        company_name = re.sub(r'\s+', ' ', company_name).strip() if company_name_tag else "Unknown Company"
        
        print(f"Scraping data for: {company_name} ({self.company_symbol})")

        # Create a folder for the company
        self._create_company_folder(company_name)

        # Scrape recent data if requested
        if scrape_recent_data:
            recent_data = soup.find(class_='col-md-7 col-sm-7 col-xs-12')
            if recent_data:
                self._scrape_company_details(recent_data)
            else:
                print("No recent data available")

        # Scrape price history if requested
        if scrape_price_history:
            self._scrape_price_history(company_name)

    def _create_company_folder(self, company_name):
        # Clean up company name by removing newlines, extra spaces, and handling parentheses
        folder_name = company_name
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        self.company_folder = folder_name

    def _scrape_company_details(self, recent_data):
        # Extract company details
        as_on_date = recent_data.find('span', class_='comp-ason').find('span', class_='text-org').text.strip()
        current_price = recent_data.find('span', class_='text-comp-green comp-price padding-second').text.strip()
        price_change_ratio = recent_data.find('span', class_='comp-ratio').text.strip()
        percentage_change = recent_data.find('span', class_='comp-percent').text.strip()

        # Open, High, Low, Volume
        open_price = recent_data.find('span', string="Open:").find_next_sibling(string=True).strip()
        high_price = recent_data.find('span', string="High:").find_next_sibling(string=True).strip()
        low_price = recent_data.find('span', string="Low:").find_next_sibling(string=True).strip()
        volume = recent_data.find('span', string="Volume:").find_next_sibling(string=True).strip()

        # 52 Week High-Low, 180 Days Average, 120 Days Average
        week_52_high_low = recent_data.find('span', string=re.compile(r"52\s*Week\s*High-Low :")).find_next_sibling(string=True).strip()
        avg_180_days = recent_data.find('span', string=re.compile(r"180\s*Days\s*Average :")).find_next_sibling(string=True).strip()
        avg_120_days = recent_data.find('span', string=re.compile(r"120\s*Days\s*Average :")).find_next_sibling(string=True).strip()

        # Save company information to CSV with 'As on date'
        self._save_company_info_to_csv(as_on_date, current_price, price_change_ratio, percentage_change,
                                       open_price, high_price, low_price, volume, week_52_high_low,
                                       avg_180_days, avg_120_days)

    def _save_company_info_to_csv(self, as_on_date, current_price, price_change_ratio, percentage_change,
                                  open_price, high_price, low_price, volume, week_52_high_low,
                                  avg_180_days, avg_120_days):
        # Create CSV file name with 'As on date'
        csv_filename = os.path.join(self.company_folder, f'{as_on_date}_company_info.csv')

        # Write company information to CSV
        with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["As on", "Current Price", "Price Change", "Percent Change", "Open Price", "High Price", 
                             "Low Price", "Volume", "52 Week High-Low", "180 Days Average", "120 Days Average"])
            writer.writerow([as_on_date, current_price, price_change_ratio, percentage_change,
                             open_price, high_price, low_price, volume, week_52_high_low, avg_180_days, avg_120_days])
        
        print(f"Company info saved as '{csv_filename}'")

    def _scrape_price_history(self, company_name):
        try:
            # Interact with the 'Price History' button
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn_cpricehistory"]'))).click()# Wait for the price history to load

            # Select "50" from the dropdown to display more rows
            select = Select(self.driver.find_element(By.NAME, 'myTableCPriceHistory_length'))
            select.select_by_value("50")
            time.sleep(3)  # Wait for the table to update

            # Create a CSV filename based on the company name with symbol
            csv_filename = os.path.join(self.company_folder, f'{company_name}_price_history.csv')

            # Open the CSV file to append data
            with open(csv_filename, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                # Append headers to CSV if the file is empty
                if file.tell() == 0:
                    html = self.driver.page_source
                    soup = BeautifulSoup(html, 'lxml')
                    price_history_table = soup.find('table', id='myTableCPriceHistory')
                    headers = [header.get_text(strip=True) for header in price_history_table.find_all('th')]
                    writer.writerow(headers)  # Write headers

                # Loop to click "Next" and append data for 5 pages
                for page in range(5):
                    html = self.driver.page_source
                    soup = BeautifulSoup(html, 'lxml')
                    price_history_table = soup.find('table', id='myTableCPriceHistory')

                    rows = []
                    for row in price_history_table.find_all('tr')[1:]:
                        cols = [col.get_text(strip=True) for col in row.find_all('td')]
                        if cols:
                            rows.append(cols)

                    # Write rows to CSV
                    writer.writerows(rows)
                    print(f"Data from page {page + 1} saved.")

                    # Click the "Next" button to go to the next page
                    next_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="myTableCPriceHistory_next"]')))
                    next_button.click()
                    time.sleep(3)  # Wait for the next page to load

            print(f"Price history data saved to '{csv_filename}'.")

        
        except TimeoutException as e:
            print(f"Timeout error: {e}")
        except NoSuchElementException as e:
            print(f"Element not found: {e}")
        except Exception as e:
            print(f"An error occurred while scraping price history: {e}")

    def quit(self):
        self.driver.quit()


# Example Usage:
if __name__ == "__main__":
    # Input company symbol (e.g., 'anlb' for Aatmanirbhar Laghubitta Bittiya Sanstha Limited)
    company_symbol = input("Enter the company symbol: ")

    # Ask the user for their scraping preferences
    scrape_recent_data = input("Do you want to scrape Recent Data? (y/n): ").strip().lower() == 'y'
    scrape_price_history = input("Do you want to scrape Price History? (y/n): ").strip().lower() == 'y'

    scraper = CompanyDataScraper(company_symbol)
    scraper.scrape_company_data(scrape_recent_data=scrape_recent_data, scrape_price_history=scrape_price_history)
    scraper.quit
