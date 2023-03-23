import json
import os
import time

import requests
import undetected_chromedriver as uc
from bs4 import BeautifulSoup


def undetected_request(link):
    options = uc.ChromeOptions()
    options.headless = True

    driver = uc.Chrome(options=options)

    driver.get(link)
    driver.implicitly_wait(10)
    driver.find_element(uc.By.CSS_SELECTOR, value='div[style="cursor: pointer;"]').click()
    time.sleep(2.5)
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, 'lxml')
    return soup


def make_request(link):
    post_body = {
        "cmd": "request.get",
        "url": link,
        "maxTimeout": 60000
    }

    response = requests.post('http://localhost:8191/v1', headers={'Content-Type': 'application/json'},
                             json=post_body)

    if response.status_code == 200:
        json_response = response.json()

        if json_response.get('status') == 'ok':
            html = json_response['solution']['response']
            soup = BeautifulSoup(html, "lxml")
            return soup

        else:
            print('Captcha Not Solved For Total Novel Pages!')

    else:
        print('Request failed For Total Novel Pages!')


def get_total_pages(novels, util):
    if novels:
        soup = make_request(util)

    else:
        soup = BeautifulSoup(util.page_source, 'lxml')

    try:
        totalPages = int(soup.select_one('div.pages a:last-child').get_text(strip=True))
    except AttributeError:
        try:
            totalPages = int(soup.select_one('div.pages span').get_text(strip=True))
        except AttributeError:
            totalPages = 1

    return totalPages


def save_data(self):
    filename = os.path.join(os.getcwd(), "data.json")
    with open(filename, 'w') as f:
        json.dump(self.data, f, indent=4)
