## Program for scraping all possible  equipment types


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

driver = webdriver.Chrome()
driver.get("https://www.auto24.ee/users/kuuluta.php?vehicle_type=101")

all_links = []

while True:
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.result-row"))
    )

    soup = BeautifulSoup(driver.page_source, "html.parser")

    links = [a["href"] for a in soup.select("div#usedVehiclesSearchResult-flex div.result-row a.row-link[href]")]
    links = ["https://www.auto24.ee" + l for l in links]
    print(f"Found {len(links)} links")
    all_links.extend(links)

    # Find next page button
    next_buttons = driver.find_elements(By.CSS_SELECTOR, "a[rel='next']")
    if next_buttons:
        driver.execute_script("arguments[0].click();", next_buttons[0])
        time.sleep(2) 
    else:
        print("Last page.")
        break

print(f"Found {len(all_links)} links in total")
driver.quit()


with open("auto24_links.csv", "w", newline="") as f:
    writer = csv.writer(f)
    for link in all_links:
        writer.writerow([link])