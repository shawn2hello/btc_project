import pyperclip
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

# SETUP SELENIUM WITH WINDOW SIZE
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.set_window_size(1920, 1080)

# OPEN PAGE
driver.get('https://intel.arkm.com/explorer/entity/microstrategy')
time.sleep(3)

# GET TOTAL PAGES
page_info_elem = driver.find_element(By.CSS_SELECTOR, 'span.Transactions_headerPageInfo__3Nhdc')
page_info_text = page_info_elem.text.strip()  # Example: "/ 195"
total_pages = int(page_info_text.replace('/', '').strip())

print(f"Total pages: {total_pages}")

with open('microstrategy_transactions_all_pages.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter='\t')  # Use tab delimiter

    header_written = False

    for page_num in range(1, total_pages + 1):
        print(f"Scraping page {page_num}")

        # CLICK COPY BUTTON
        copy_button = driver.find_element(By.CSS_SELECTOR, 'div.Transactions_csvButtonsContainer__f5GSE svg')
        copy_button.click()
        time.sleep(1.5)

        # GET CLIPBOARD DATA
        copied_text = pyperclip.paste()

        lines = copied_text.strip().split('\n')
        for i, line in enumerate(lines):
            row = line.split('\t')
            if i == 0:
                if not header_written:
                    writer.writerow(row)
                    header_written = True
            else:
                writer.writerow(row)

        # GO TO NEXT PAGE
        if page_num < total_pages:
            chevrons = driver.find_elements(By.CSS_SELECTOR, 'svg.Transactions_chevron__EfxUX')
            if len(chevrons) >= 2:
                chevrons[1].click()
                time.sleep(5)
            else:
                print("No next page button found.")
                break

driver.quit()
