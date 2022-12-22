####################################
#        SCRAP SNB PDF DATA
####################################

# In this script, we download all pdf's from the SNB homepage that contain the policy announcements at the time
# of the interest rate decision. We scrap the documents in English, French and German.

# IMPORTS
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from selenium.common.exceptions import TimeoutException

import chromedriver_autoinstaller as chr
chr.install()

# DEFINE THE WORKING DIRECTORY TO BE THE FOLDER PROJECT:
# * « * * « * * « * * « * * « * * « * * « * * « * * « * * « * * « * * « * * « *
os.chdir("INDICATE WORKING DIRECTORY")
wkdir = os.getcwd()

path_pdf = wkdir + "INDICATE DOWNLOAD FOLDER"
# * « * * « * * « * * « * * « * * « * * « * * « * * « * * « * * « * * « * * « *


options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
    "download.default_directory": path_pdf,  # Change default directory for downloads
    "download.prompt_for_download": False,  # To auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True  # It will not show PDF directly in chrome
})

# START WEBBOWSER
driver = webdriver.Chrome(options=options)

languages = ["de", "fr", "en"]
#languages = ["en"]

def get_all_links(driver, lang):
    links = []

    if lang == "de":
        elements = driver.find_elements(By.XPATH, "//h3[contains(., 'Geldpolitische Lage') or contains(., 'Geldpolitische Beschlüsse')]//ancestor::a[1]")
    elif lang == "fr":
        elements = driver.find_elements(By.XPATH, "//h3[contains(., 'situation économique et ') or contains(., 'La politique monétaire') or contains(., 'Examen du')  or contains(., 'Décisions de politique monétaire')]//ancestor::a[1]")
    elif lang == "en":
        elements = driver.find_elements(By.XPATH, "//h3[contains(., 'Monetary policy ass') or contains(., 'Monetary policy decis') or contains(., 'assessment of monetary policy')]//ancestor::a[1]")

    for elem in elements:
        href = elem.get_attribute("href")
        links.append(href)
    return links

# ---------------------------
# LOOP THROUGH ALL LANGUAGES
# ---------------------------


for language in languages:

    if language == "de":
        driver.get("https://www.snb.ch/de/ifor/media/id/media_releases?dsrp_7jpar4yij.page=1")
    elif language == "fr":
        driver.get("https://www.snb.ch/fr/ifor/media/id/media_releases?dsrp_7jpar4yij.page=1")
    elif language == "en":
        driver.get("https://www.snb.ch/en/ifor/media/id/media_releases?dsrp_7jpar4yij.page=1")

    # define main window:
    main_window = driver.current_window_handle

    time.sleep(1)

    links = get_all_links(driver=driver, lang=language)

    for l in links:
        print(l)
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        # check whether file already exists:
        check = l.split("source/", 1)[1]
        filepath = os.path.join(path_pdf, check)
        print(str(filepath))
        if os.path.exists(filepath):
            print("file already downloaded")
            driver.close()
            driver.switch_to.window(main_window)
        else:
            driver.get(l)
            time.sleep(1)
            driver.close()
            driver.switch_to.window(main_window)

    # now, loop through all other pages: (however, set a maximum of trials)
    for i in range(1, 50):
        try:
            elm = driver.find_element(By.CSS_SELECTOR, '.next')
            if 'inactive' in elm.get_attribute('class'):
                break

            elm.click()

            links = get_all_links(driver=driver, lang=language)

            for l in links:
                print(l)
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                # check whether file already exists:
                check = l.split("source/", 1)[1]
                filepath = os.path.join(path_pdf, check)
                print(str(filepath))
                if os.path.exists(filepath):
                    print("file already downloaded")
                    driver.close()
                    driver.switch_to.window(main_window)
                else:
                    driver.get(l)
                    time.sleep(2)
                    driver.close()
                    driver.switch_to.window(main_window)

        except TimeoutException:
            break


driver.quit()


