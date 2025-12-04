from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time




## ----------------------------------------------------------------- ADD-ON COLUMNS ----------------------------------------------------------------------------- 



binaryAddons = ["abs pidurid", "elektrooniline seisupidur", "turvakardinad", "kõrvalistuja turvapadja väljalülitamise võimalus", 
          "juhi väsimuse tuvastamise süsteem", "sõiduraja vahetamise abisüsteem", "liiklusmärkide tuvastus ja kuvamine", "öise nägemise assistent",
          "pimenurga hoiatus", "jalakäija ohutusfunktsiooniga kapott", "lisapidurituli", "vihmasensor", "integreeritud lapseiste",
          "turvavööde eelpingutid esiistmetel", "automaatne paigalseismise funktsioon / mägistardi abi",
          "laser", "esitulede pesurid", "kurvituled", "päevasõidutulede automaatne lülitus", 
          "kaugtulede ümberlülitamise assistent", "tulede korrektor", "valgustuspakett",
          "rehvirõhu kontrollsüsteem", "multifunktsionaalne rool", "nahkkattega rool", "sportrool", 
          "soojendusega rool", "käiguvahetus roolilt", "parempoolne rool (vasakpoolne liiklus)",
          "apple carplay", "android auto", "dvd", "elektriline antenn", "autokompuuter",
          "gsm antenn", "taskud esiistmete seljatugedes", "sahtlid esiistmete all", "pagasiruumi matt",
          "nahkkattega käigukanginupp", "nahkkattega käsipidurikang", "tume laepolster", 
          "kaassõitja istme seljatugi allaklapitav", "tagaistme seljatugi allaklapitav",
          "comfort istmed", "sportistmed", "kliimaautomaatik", "konditsioneer", "virtuaalsed välispeeglid",
          "virtuaalne sisepeegel", "toonitud klaasid", "panoraamkatus (klaasist)", "uste servosulgurid",
          "võtmeta avamine", "võtmeta käivitus", "salongi lisasoojendus", "integreeritud väravapult",
          "eraldi kliimaseade tagaistmetele", "uste sisevalgustus", "kohtvalgustid", "automaatse parkimise funktsioon",
          "coming-/leaving-home funktsioon", "digitaalne näidikutepaneel", "info kuvamine esiklaasile",
          "pakiruumi liugpõrand", "elektrilised liuguksed", "telefoni juhtmevaba laadimine", "tagaspoiler",
          "esispoiler", "spoileriring", "sportvedrustus", "sportsummuti", "õhkvedrustus", "start-stopp süsteem", "suusakott", "rehviparanduskomplekt", "jahutusega kindalaegas", "välistemperatuuri näidik", 
          "elektrilise soojendusega esiklaas", "tagaklaasi soojendus", "aknapesupihustite sulatus", "pagasi võrk pakiruumis", "salongi ja pakiruumi eraldusvõrk", "kaubakinnituse konksud",
          "tagaklaasi puhasti", "paigaldatud tulekustuti", "haagise stabiliseerimissüsteem", "reisiarvesti",
          "esi- ja tagarataste porikummid", "invavarustus", "4-ratta pööramine", "arvel kui n1 kaubik", "kesklukustus",
          "kesklukustus (puldiga)", "isofix lasteistme kinnitus", "isofix lasteistme kinnitus (ees)",
          "isofix lasteistme kinnitus (taga)", "isofix lasteistme kinnitus (ees, taga)", "xenon", "xenon (lähituled)", "xenon (kaugtuled)", "xenon (lähituled, kaugtuled)", "led", 
          'led (päevatuled)', 'led (päevatuled, tagatuled)', 'led (päevatuled, tagatuled, lähituled)', 
          'led (päevatuled, tagatuled, lähituled, kaugtuled)', 'led (tagatuled)', 'led (tagatuled, lähituled)', 
          'led (tagatuled, lähituled, kaugtuled)', 'led (lähituled)', 'led (lähituled, kaugtuled)', 'led (kaugtuled)',
          "udutuled", 'udutuled (eesmised)', 'udutuled (eesmised, tagumine)', 'udutuled (eesmised, tagumine, kurvitule funktsiooniga)',
          'udutuled (tagumine)', 'udutuled (tagumine, kurvitule funktsiooniga)', 'udutuled (kurvitule funktsiooniga)',
          "reguleeritav roolisammas", 'reguleeritav roolisammas (kõrgus ja sügavus)', 'reguleeritav roolisammas (kõrgus ja sügavus, elektriliselt)', 
          'reguleeritav roolisammas (kõrgus ja sügavus, elektriliselt, mäluga)', 'reguleeritav roolisammas (elektriliselt)', 
          'reguleeritav roolisammas (elektriliselt, mäluga)', 'reguleeritav roolisammas (mäluga)', "navigatsiooniseade",
          'navigatsiooniseade (kaardiga)', 'navigatsiooniseade (kaardiga, hääljuhtimisega)', 'navigatsiooniseade (hääljuhtimisega)',
          "jalamatid", 'jalamatid (tekstiilist)', 'jalamatid (tekstiilist, kummist)', 'jalamatid (tekstiilist, kummist, veluurist)', 
          'jalamatid (kummist)', 'jalamatid (kummist, veluurist)', 'jalamatid (veluurist)', "topsihoidjad", "topsihoidjad (ees, taga)",
          "topsihoidjad (taga)", "topsihoidjad (ees)", "istmed reguleeritava kõrgusega", "istmed reguleeritava kõrgusega (juhiiste, kõrvalistuja iste)",
          "istmed reguleeritava kõrgusega (juhiiste)", "istmed reguleeritava kõrgusega (kõrvalistuja iste)", "käetugi ees",
          "käetugi ees (laekaga)", "käetugi taga", "käetugi taga (laekaga)", "elektrilised välispeeglid", 'elektrilised välispeeglid (soojendusega)',
          'elektrilised välispeeglid (soojendusega, kokkuklapitavad)', 'elektrilised välispeeglid (soojendusega, kokkuklapitavad, mäluga)', 
          'elektrilised välispeeglid (kokkuklapitavad)', 'elektrilised välispeeglid (kokkuklapitavad, mäluga)', 'elektrilised välispeeglid (mäluga)',
          "püsikiiruse hoidja", "püsikiiruse hoidja (eessõitjaga distantsi hoidev)", "pakiruumi avamine elektriliselt", 
          "pakiruumi avamine elektriliselt (puldist, jalaviipega)", "pakiruumi avamine elektriliselt (puldist)", 
          "pakiruumi avamine elektriliselt (jalaviipega)", "rulookardin tagaaknal", "rulookardin tagaaknal (elektriline)",
          "automaatselt tumenevad peeglid", "automaatselt tumenevad peeglid (sees, väljas)", "automaatselt tumenevad peeglid (sees)",
          "automaatselt tumenevad peeglid (väljas)", "parkimisandurid", "parkimisandurid (ees, taga)",
          "parkimisandurid (ees)", "parkimisandurid (taga)", "parkimiskaamera", "parkimiskaamera (360)", "reguleeritav vedrustus",
          'reguleeritav vedrustus (elektriliselt)', 'reguleeritav vedrustus (elektriliselt, jäikus)', 
          'reguleeritav vedrustus (elektriliselt, jäikus, kõrgus)', 'reguleeritav vedrustus (jäikus)', 
          'reguleeritav vedrustus (jäikus, kõrgus)', 'reguleeritav vedrustus (kõrgus)', "pagasikate", "pagasikate (automaatne)",
          "veokonks", "veokonks (elektriline, teisaldatav)", "veokonks (teisaldatav)", "veokonks (elektriline)"
          ]

binaryWithAdditionalInfo = ["immobilisaator", "stabiilsuskontroll", "pidurdusjõukontroll", "veojõukontroll", "sõiduraja hoidmise abisüsteem", 
          "kokkupõrget ennetav pidurisüsteem", "automaatpidurdussüsteem", "mägipidur", "lisatuled", "suverehvid", "ilukilbid", "tagavararatas", 
          "helivõimendi", "kõlarid", "subwoofer", "cd box", "autotelefon", "käed vabad süsteem", "nahkpolster", "poolnahkpolster", 
          "veluurpolster", "tekstiilpolster", "mootori eelsoojendus", "salongi eelsoojendus", "katusereelingud", "topeltklaasid"
          ]

numeralAddons = ["turvapadi", "elektriliselt reguleeritavad istmed", "õhuga reguleeritav iste", "istmesoojendused", "elektrilised akende tõstukid",
           "peeglid päikesesirmides", "rulookardinad ustel", "12v pistikupesad"]

allAddons = binaryAddons + binaryWithAdditionalInfo + numeralAddons

## ------------------------------------------------------------------------------------------------------------------------------------------------

links = pd.read_csv("auto24_links.csv", header=None)[0].tolist()[8117:]

driver = webdriver.Chrome()
columns = ["Link", "Mark", "Mudel", "Täisnimi"] + allAddons
batch = []
start = time.perf_counter()
batch_size = 3000
first_write = True
batch_nr = 1

for i, link in enumerate(links):
    try:
        try:
            driver.get(link)
        except:
            print(f"VIGA LINGI NR {i} ({link}) LAADIMISEGA")
            time.sleep(30)
        try:
            driver.get(link)
            # Wait untill last section has loaded
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.section.vTechData"))
            )
        except:
            pass
        data = {}
        data["Link"] = link

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

        # --- ADDONS ---
        extras = driver.find_elements(By.CSS_SELECTOR, "div.section.vEquipment li.item")
        for e in extras:
            addonHTML = e.text.strip().lower()

            if addonHTML in binaryAddons:
                data[addonHTML] = 1
                continue
            
            found = False
            for addon in binaryWithAdditionalInfo:
                if addon in addonHTML:       
                    data[addon] = 1
                    found = True
                    break

            if found:
                continue

            for addon in numeralAddons:
                if addon in addonHTML:
                    nr = addonHTML.split()[0]
                    data[addon] = nr
                    break
                

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

        batch.append(data)

        if len(batch) >= batch_size:
            df = pd.DataFrame(batch)
            for col in columns:
                if col not in df.columns:
                    df[col] = 0
            df = df[columns]

            df.to_csv(
                "auto24_data8000.csv",
                index=False,
                mode="w" if first_write else "a",
                header=first_write
            )
            first_write = False
            batch = []
            end = time.perf_counter()
            print("Tehtud ", batch_nr, "Kulunud aeg:", end - start, "sekundit")
            batch_nr += 1
            start = time.perf_counter()

    except Exception as e:
        print("VIGA linkiga:", link)
        print("Error:", e)
        continue

driver.quit()

if batch:
    df = pd.DataFrame(batch)
    df.to_csv("auto24_data2.csv", index=False, mode="w", header=False)

