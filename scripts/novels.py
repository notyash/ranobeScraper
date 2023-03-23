import json
import os
import time
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup


class NovelScraper:
    def __init__(self):
        os.chdir('../Output')
        with open('data.json', 'r') as file:
            self.data = json.loads(file.read())

    @staticmethod
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

    @staticmethod
    def generate_page_links(start_page, new_pages):
        links = []
        for page in range(start_page, start_page + new_pages + 1):
            links.append(f"https://ranobes.net/novels/page/{page}/")

        return links

    def save_links(self, soup, link):
        for element in soup.select("h2.title"):
            self.data[element.text] = {'link': element.find("a")['href']}

        print(link.split('/')[-2], end="|", flush=True)

    def save_data(self):
        filename = os.path.join(os.getcwd(), "data.json")
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def new_data_found(self, link):
        print('Checking For New Novels..')
        soup = self.make_request(link)

        try:
            newTotalPages = int(soup.select_one('div.pages a:last-child').get_text(strip=True))
        except Exception as e:
            print(e)
            newTotalPages = int(soup.select_one('div.pages span').get_text(strip=True))

        old_total_pages = self.data['Total Novel Pages']
        self.data['Total Novel Pages'] = newTotalPages

        if old_total_pages >= newTotalPages:
            print('No New Novels Found.')
            return False, False, False

        newPages = newTotalPages - old_total_pages
        print(f'{newPages} New Novel Page(s) Found. Scraping Data..\n')
        return True, newPages, newTotalPages - newPages

    def fetch_links(self, link):
        soup = self.make_request(link)

        self.save_links(soup, link)

    def update_chapter_links(self):
        for key in self.data.keys():
            if key != 'Total Novel Pages':
                novel_id = self.data[key]['link'].split('/')[-1].split('-')[0]
                self.data[key]['Chapter Link'] = f"https://ranobes.net/chapters/{novel_id}/page/1/"
        self.save_data()


def find_novels(scraper):
    start_time = time.time()
    true, new_pages, start_page = scraper.new_data_found('https://ranobes.net/novels/page/1/')
    if not true:
        print(f"\nTotal Time Taken For Novels:{time.time() - start_time}\n")
        return

    page_links = scraper.generate_page_links(start_page, new_pages)

    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(scraper.fetch_links, page_links)

    scraper.update_chapter_links()
    print(f"\nTotal Time Taken For Novels:{time.time() - start_time}\n")
    return


def run_novel_scraper():
    scraper = NovelScraper()
    find_novels(scraper)


# 376.31 thread test 1
# 346.31 thread test 2
