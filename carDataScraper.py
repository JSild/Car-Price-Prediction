from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

links = ["https://www.auto24.ee/soidukid/4209894",
"https://www.auto24.ee/soidukid/4256941",
"https://www.auto24.ee/soidukid/4256957",
"https://www.auto24.ee/soidukid/3134721",
"https://www.auto24.ee/soidukid/4245490",
"https://www.auto24.ee/soidukid/4256886",
"https://www.auto24.ee/soidukid/4257538",
"https://www.auto24.ee/soidukid/4253130",
"https://www.auto24.ee/soidukid/4255677",
"https://www.auto24.ee/soidukid/4253217"]
driver = webdriver.Chrome()
all_data = []
columns = ["Mark", "Mudel", "Täisnimi"]
for link in links:
    driver.get(link)

    try:
        # Wait untill last section has loaded
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.section.vTechData"))
        )
    except:
        pass
    data = {}

    # --- MARK JA MUDEL ---
    crumbs = driver.find_elements(By.CSS_SELECTOR, "div.b-breadcrumbs a")
    data["Mark"] = crumbs[1].text.strip() if len(crumbs) > 1 else ""
    data["Mudel"] = crumbs[-2].text.strip() if len(crumbs) > 1 else ""

    # --- TÄISNIMI ---
    try:
        data["Täisnimi"] = driver.find_element(By.CSS_SELECTOR, "h1.commonSubtitle").text.split('\n')[0]
    except:
        data["Täisnimi"] = ""

    # --- PÕHIANDMED (tabel) ---
    main_data = driver.find_elements(By.CSS_SELECTOR, "table.main-data tr")

    for row in main_data:
        try:
            label = row.find_element(By.CSS_SELECTOR, "td.label").text.strip().replace(":", "")
            value = row.find_element(By.CSS_SELECTOR, "td.field").text.strip()
            if label.lower() == "soodushind":
                data["Hind"] = value
            elif label.lower() not in ["reg. number", "vin-kood"]: # Dont need these
                data[label] = value
                if label not in columns:
                    columns.append(label)
                
        except:
            continue
    data["Hind"] = data["Hind"].split("\n")[0]

    # --- LISAD / VARUSTUS ---
    extras = driver.find_elements(By.CSS_SELECTOR, "div.section.vEquipment li.item")
    for e in extras:
        txt = e.text.strip()
        if txt:
            data[txt] = 1
            if txt not in columns:
                columns.append(txt)
    
    # --- TECHNICAL DATA ---

    labels = driver.find_elements(By.CSS_SELECTOR, "div.section.vTechData td.label")
    values = driver.find_elements(By.CSS_SELECTOR, "div.section.vTechData td.value")

    for i in range(min(len(labels), len(values))):
        label = labels[i].text.strip().replace(":", "")
        value = values[i].text.strip()
        if label and value:
            data[label] = value
            if label not in columns:
                columns.append(label)

    all_data.append(data)
    print(data)

driver.quit()

# --- MUUDA PANDAS DATAFRAME-KS ---
df = pd.DataFrame(all_data)

# Lisa tulpade järjekord (et kõik lisad oleks sees)
for col in columns:
    if col not in df.columns:
        df[col] = 0

# Täida puuduvad väärtused nullidega
df = df[columns].fillna(0)

# --- SALVESTA CSV ---
df.to_csv("auto24_data1.csv", index=False, encoding="utf-8")
print(f"Salvestatud {len(df)} rida ja {len(df.columns)} tulpa.")
