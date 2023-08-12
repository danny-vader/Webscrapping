import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

class_ids = {
    "category": "css-1tfboal",
    "article": "css-18i7m94",
    "article_heading": "css-gm5mek",
    "article_text": "css-z84tn2",
}


def init_driver():
    try:
        driver = webdriver.Firefox()
        driver.wait = WebDriverWait(driver, 5)
        return driver
    except Exception as e:
        print(e)
        return None


def load_website(driver, url):
    try:
        driver.get(url)
        sleep(2)
        return True
    except:
        return False


counter = 0


def get_data(url):
    driver = init_driver()

    if driver is None:
        print("Error: Driver not initialized")
        return

    website_loaded = load_website(driver, url)

    if not website_loaded:
        print("Error: Website not loaded")
        return

    try:
        os.mkdir("edutopia")
    except:
        print("Error: Directory already exists")

    categories = driver.find_elements(By.CLASS_NAME, class_ids["category"])
    l = len(categories)

    for i in range(l):
        category = driver.find_elements(
            By.CLASS_NAME, class_ids["category"])[i]
        category_name = category.text
        category_name = category_name.replace('/', '-')
        category_name = category_name.replace(':', '-')
        print(category_name)

        try:
            os.mkdir("edutopia/{}".format(category_name))
        except:
            print("Error: Directory already exists")
            continue

        category.click()
        sleep(2)

        articles = driver.find_elements(By.CLASS_NAME, class_ids["article"])
        sleep(2)
        text_to_be_found = []

        for article in articles:
            heading = article.find_element(
                By.CLASS_NAME, class_ids["article_heading"])
            text = article.find_element(
                By.CLASS_NAME, class_ids["article_text"])
            text_to_be_found.append(
                {"heading": heading.text, "text": text.text})
            sleep(2)

        j = 0
        for text in text_to_be_found:
            f = open(
                'edutopia/{}/{}.json'.format(category_name, j), 'x')
            j += 1
            json.dump(text, f)
            f.close()

        driver.get(url)
        sleep(3)


url = "https://www.edutopia.org/topic-index"

get_data(url)
