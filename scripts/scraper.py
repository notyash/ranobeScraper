import json
import os
import time
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self):
        self.novels = {'Total Pages': 0}
        os.chdir('./Output')
        with open('data.json', 'r') as file:
            self.data = json.loads(file.read())

    @staticmethod
    def generate_page_links(start_page, count):
        links = []
        for page in range(start_page, start_page + count + 1):
            links.append(f"https://ranobes.net/novels/page/{page}/")

        return links

    def save_novel_links(self, soup):
        for element in soup.select("h2.title"):
            self.novels[element.text] = element.find("a")['href']

    def save_data(self):
        filename = os.path.join(os.getcwd(), "data.json")
        with open(filename, 'w') as f:
            json.dump(self.novels, f, indent=4)

    def new_pages_found(self, link):
        print('Checking for new pages..')

        url = link
        post_body = {
            "cmd": "request.get",
            "url": url,
            "maxTimeout": 60000
        }
        response = requests.post('http://localhost:8191/v1', headers={'Content-Type': 'application/json'},
                                 json=post_body)

        if response.status_code == 200:
            json_response = response.json()

            if json_response.get('status') == 'ok':
                html = json_response['solution']['response']
                soup = BeautifulSoup(html, "lxml")
                totalPages = int(soup.select_one('div.pages a:last-child').get_text(strip=True))
                self.novels['Total Pages'] = totalPages
                if self.data['Total Pages'] >= totalPages:
                    print('Data already scraped.')
                    return False, False, False

                newPages = totalPages - self.data['Total Pages']
                print(f'{newPages + 1} New pages found. Scraping Data..\n')
                return True, newPages, totalPages-newPages
            else:
                print('Captcha Not Solved For Total Pages!')

        else:
            print('Request failed For Total Pages!')

    def fetch_links(self, link):
        url = link
        post_body = {
            "cmd": "request.get",
            "url": url,
            "maxTimeout": 60000
        }

        response = requests.post('http://localhost:8191/v1', headers={'Content-Type': 'application/json'},
                                 json=post_body)

        if response.status_code == 200:
            json_response = response.json()

            if json_response.get('status') == 'ok':
                html = json_response['solution']['response']
                soup = BeautifulSoup(html, "lxml")

                self.save_novel_links(soup)
                self.save_data()
                print(link.split('/')[-2], end="|", flush=True)
            else:
                print('Captcha Not Solved')

        else:
            print('Request failed!')


def main():
    scraper = Scraper()
    true, new_pages, start_page = scraper.new_pages_found('https://ranobes.net/novels/page/1/')
    if not true:
        return
    start_time = time.time()
    page_links = scraper.generate_page_links(start_page, new_pages)

    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(scraper.fetch_links, page_links)

    print("\n\tTotal Time Taken:", time.time() - start_time)


if __name__ == '__main__':
    main()

# 376.31 thread test 1
# 346.31 thread test 2

# todo remove unnecessary characters from json data
