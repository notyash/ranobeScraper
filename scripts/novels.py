import json
import time
from concurrent.futures import ThreadPoolExecutor

from scripts.utils import make_request, get_total_pages, save_data


class NovelScraper:
    def __init__(self):
        with open('data/data.json', 'r') as file:
            self.data = json.loads(file.read())

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

    def newNovelsFound(self):
        print('Checking For New Novels..')
        newTotalPages = get_total_pages(True, 'https://ranobes.net/novels/page/1/')

        if self.data.get('Total Novel Pages') is None:
            self.data['Total Novel Pages'] = 0

        old_total_pages = self.data['Total Novel Pages']
        if old_total_pages >= newTotalPages:
            print('No New Novels Found.')
            return False, False, False
        else:
            print('New Novels Found')
            self.data['Total Novel Pages'] = newTotalPages
            newPages = newTotalPages - old_total_pages
            print(f'{newPages} New Novel Page(s) Found. Scraping Data..\n')
            return True, newPages, newTotalPages - newPages

    def fetch_links(self, link):
        soup = make_request(link)

        self.save_links(soup, link)

    def update_chapter_links(self):
        for key in self.data.keys():
            if key != 'Total Novel Pages':
                novel_id = self.data[key]['link'].split('/')[-1].split('-')[0]
                self.data[key]['Chapter Link'] = f"https://ranobes.net/chapters/{novel_id}/page/1/"

    def find_novels(self):
        start_time = time.time()
        true, new_pages, start_page = self.newNovelsFound()
        if not true:
            print(f"\nTotal Time Taken For Novels:{time.time() - start_time}\n")
            return

        page_links = self.generate_page_links(start_page, new_pages)
        with ThreadPoolExecutor(max_workers=8) as executor:
            executor.map(self.fetch_links, page_links)

        self.update_chapter_links()
        save_data(self)

        print(f"\nTotal Time Taken For Novels:{time.time() - start_time}\n")
        return


def run_novel_scraper():
    scraper = NovelScraper()
    scraper.find_novels()
