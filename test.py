# from csv import DictReader
#
import json

import requests
# import asyncio
# import time
# from selenium.webdriver.support.ui import WebDriverWait
#
# import undetected_chromedriver as uc
from bs4 import BeautifulSoup


# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
#
#
# def get_cookies(file):
#     with open(file, encoding='utf-8-sig') as f:
#         reader = DictReader(f)
#         list_of_dicts = list(reader)
#
#     return list_of_dicts
#
#
def test():
    # scraper = cloudscraper.create_scraper(
    #     browser={'browser': 'chrome'}, delay=10)
    #
    # r = scraper.get('http://ranobes.top/novels/1205835-circle-of-inevitability-v741610.html', cookies=ccookies,
    #                 headers=headers, timeout=(3.05, 27))
    # print(r.text)
    post_body = {
        "cmd": "request.get",
        "url": 'https://ranobes.net/i-only-learn-forbidden-skills-v741610-1205799/2081166.html',
        "maxTimeout": 60000
    }
    response = requests.post('http://localhost:8191/v1',
                             headers={'Content-Type': 'application/json'}, json=post_body)
    response.raise_for_status()

    if response.status_code == 200:
        json_response = response.json()
        if json_response.get('status') == 'ok':
            html = json_response['solution']['response']
            soup = BeautifulSoup(html, 'lxml')
            body = ''
            for p in soup.select('div#arrticle p'):
                body += p.text + '\n\n'
            return body


# body = test()
# print(body)
with open('Output/data.json', 'r') as file:
    data = json.loads(file.read())
name = 'Circle of Inevitability'
link = 'https://ranobes.net/circle-of-inevitability-v741610-1205835/2102202.html'
chapter = data[name]['Chapter Links']
chapter.reverse()
print(chapter.index(link) + 1)

# def selenium_test(start_url):
#     options = uc.ChromeOptions()
#     options.headless = True
#     driver = uc.Chrome(options=options)
#     driver.get(start_url)
#
#     WebDriverWait(driver, 5).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, 'div[style="cursor: pointer;"]'))).click()
#     time.sleep(3)
#
#     soup = BeautifulSoup(driver.page_source, 'lxml')
#
#     try:
#         totalPages = int(soup.select_one('div.pages a:last-child').get_text(strip=True))
#     except AttributeError:
#         try:
#             totalPages = int(soup.select_one('div.pages span').get_text(strip=True))
#         except AttributeError:
#             totalPages = 1
#
#     chapters = {}
#     currentPage = 0
#     while currentPage < totalPages:
#         soup = BeautifulSoup(driver.page_source, 'lxml')
#
#         for element in soup.select('div.cat_block.cat_line'):
#             chapters[element.text.split(":")[0]] = element.find('a')['href']
#
#         WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.page_next'))).click()
#         currentPage += 1
#         print(f"Page {currentPage} done.")
#
#     driver.quit()
#     return chapters
#
#
# html = selenium_test('https://ranobes.net/chapters/1205835/')
# print(html)
