# # from csv import DictReader
# #
#
# # import asyncio
# import json
# import time
#
# #
# import undetected_chromedriver as uc
# from bs4 import BeautifulSoup
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
#
#
# #
# #
# # def get_cookies(file):
# #     with open(file, encoding='utf-8-sig') as f:
# #         reader = DictReader(f)
# #         list_of_dicts = list(reader)
# #
# #     return list_of_dicts
# #
# #
# # def test():
# #     # scraper = cloudscraper.create_scraper(
# #     #     browser={'browser': 'chrome'}, delay=10)
# #     #
# #     # r = scraper.get('http://ranobes.top/novels/1205835-circle-of-inevitability-v741610.html', cookies=ccookies,
# #     #                 headers=headers, timeout=(3.05, 27))
# #     # print(r.text)
# #     post_body = {
# #         "cmd": "request.get",
# #         "url": 'https://ranobes.net/i-only-learn-forbidden-skills-v741610-1205799/2081166.html',
# #         "maxTimeout": 60000
# #     }
# #     response = requests.post('http://localhost:8191/v1',
# #                              headers={'Content-Type': 'application/json'}, json=post_body)
# #     response.raise_for_status()
# #
# #     if response.status_code == 200:
# #         json_response = response.json()
# #         if json_response.get('status') == 'ok':
# #             html = json_response['solution']['response']
# #             soup = BeautifulSoup(html, 'lxml')
# #             body = ''
# #             for p in soup.select('div#arrticle p'):
# #                 body += p.text + '\n\n'
# #             return body
# #
#
# # body = test()
# # print(body)
#
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
#     chapters = dict()
#     currentPage = 0
#     totalPages = 2
#     while currentPage < totalPages:
#         soup = BeautifulSoup(driver.page_source, 'lxml')
#         scripts = soup.find_all('script')
#         dictionary_text = str(scripts[6]).replace('<script>window.__DATA__ = ', '').replace('</script>', '')
#         data = json.loads(dictionary_text)
#         for i in range(len(data['chapters'])):
#             chapters[data['chapters'][i]['title']] = data['chapters'][i]['link']
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
# print(len(html))
dict = {
            "Chapter 16: My Overly Competent Subordinates Are Driving Me Crazy (4)": "https://ranobes.net/im-not-that-kind-of-talent-v741610-1205815/2097133.html",
            "Chapter 15: My Overly Competent Subordinates Are Driving Me Crazy (3)": "https://ranobes.net/im-not-that-kind-of-talent-v741610-1205815/2092538.html",
            "Chapter 14: My Overly Competent Subordinates Are Driving Me Crazy (2)": "https://ranobes.net/im-not-that-kind-of-talent-v741610-1205815/2090130.html",
            "Chapter 13: My Overly Competent Subordinates Are Driving Me Crazy (1)": "https://ranobes.net/im-not-that-kind-of-talent-v741610-1205815/2085095.html",
            "Chapter 12: Heroes, Meetings, And\u2026 (3)": "https://ranobes.net/im-not-that-kind-of-talent-v741610-1205815/2085094.html",
            "Chapter 11: Heroes, Meetings, And\u2026 (2)": "https://ranobes.net/im-not-that-kind-of-talent-v741610-1205815/2085092.html",
            "Chapter 10: Heroes, Meetings, And\u2026 (1)": "https://ranobes.net/im-not-that-kind-of-talent-v741610-1205815/2085091.html",
            "Chapter 9: Zero Corps Commander Deon Hart (7)": "https://ranobes.net/im-not-that-kind-of-talent-v741610-1205815/2085090.html",
            "Chapter 8: Zero Corps Commander Deon Hart (6)": "https://ranobes.net/im-not-that-kind-of-talent-v741610-1205815/2085089.html",
            "Chapter 7: Zero Corps Commander Deon Hart (5)": "https://ranobes.net/im-not-that-kind-of-talent-v741610-1205815/2085088.html",
            "Chapter 6: Zero Corps Commander Deon Hart (4)": "https://ranobes.net/im-not-that-kind-of-talent-v741610-1205815/2085087.html",
            "Chapter 5: Zero Corps Commander Deon Hart (3)": "https://ranobes.net/im-not-that-kind-of-talent-v741610-1205815/2085086.html",
            "Chapter 4: Zero Corps Commander Deon Hart (2)": "https://ranobes.net/im-not-that-kind-of-talent-v741610-1205815/2085085.html",
            "Chapter 3: Zero Corps Commander Deon Hart (1)": "https://ranobes.net/im-not-that-kind-of-talent-v741610-1205815/2085093.html",
            "Chapter 2: The Demon King\u2019s Strongest Hand (2)": "https://ranobes.net/im-not-that-kind-of-talent-v741610-1205815/2085084.html",
            "Chapter 1: The Demon King\u2019s Strongest Hand (1)": "https://ranobes.net/im-not-that-kind-of-talent-v741610-1205815/2085082.html"
        }
print(list(dict.items())[:4])