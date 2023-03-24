import json
import time
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from scripts.data import DataScraper
from scripts.utils import undetected_request, make_request, get_total_pages, save_data


class ChapterScraper(DataScraper):
    def __init__(self):
        super().__init__()

    def generateChapterLinks(self, name, start_url):
        options = uc.ChromeOptions()
        options.headless = True
        driver = uc.Chrome(options=options)
        driver.get(start_url)

        WebDriverWait(driver, 5).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'div[style="cursor: pointer;"]'))).click()
        time.sleep(2.5)

        totalPages = get_total_pages(False, driver)

        chapters = dict()
        currentPage = 0
        while currentPage < totalPages:
            soup = BeautifulSoup(driver.page_source, 'lxml')
            scripts = soup.find_all('script')
            dictionary_text = str(scripts[6]).replace('<script>window.__DATA__ = ', '').replace('</script>', '')
            data = json.loads(dictionary_text)
            for i in range(len(data['chapters'])):
                chapters[data['chapters'][i]['title']] = data['chapters'][i]['link']

            try:
                WebDriverWait(driver, 2).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, 'span.page_next'))).click()
                currentPage += 1
                print(f"Page {currentPage} done.")
            except TimeoutException:
                break
        driver.quit()
        self.data[name]['Chapter Links'] = chapters
        self.data[name]['Total Chapters'] = len(chapters)

    def get_total_chapters(self, name):
        soup = undetected_request(self.data[name]['Chapter Link'])
        try:
            total_chapters = int(soup.select_one('h6.title').text.split(':')[0].split(' ')[-1])
        except ValueError:
            total_chapters = int(float(soup.select_one('h6.title').text.split(' ')[-1]))

        return total_chapters

    def newChaptersFound(self, name, start_url):
        new_total_chapters = self.get_total_chapters(name)
        if self.data[name].get('Total Chapters') is not None:
            old_total_chapters = self.data[name]['Total Chapters']
            if old_total_chapters >= new_total_chapters:
                print('No New Chapters Found.')
                return False, None
            else:
                print('New Chapters Found.')
                self.data[name]['Total Chapters'] = new_total_chapters
                newChapters = new_total_chapters - old_total_chapters
                return True, newChapters
        else:
            self.generateChapterLinks(name, start_url)
            return True, None

    def save_chapters(self, soup, chapter, name):
        body = ''
        for p in soup.select('div#arrticle p'):
            body += p.text + '\n\n'

        self.data[name][chapter] = body

    def fetch_chapters(self, name, link):
        soup = make_request(link[1])
        chapter = link[0]
        self.save_chapters(soup, chapter, name)

        print('.', end="|", flush=True)

    def find_chapters(self, scraper, name):
        print('Getting Chapters..')
        start_time = time.time()
        start_url = self.data[name]['Chapter Link'].replace('100000', '1')
        true, chaptersFound = scraper.newChaptersFound(name, start_url)
        if not true:
            print(f"\nTotal Time Taken For Chapters:{time.time() - start_time}\n")
            return

        if chaptersFound is not None:
            links = list(self.data[name]['Chapter Links'].items())[:chaptersFound]
            with ThreadPoolExecutor(max_workers=8) as executor:
                executor.map(scraper.fetch_chapters, repeat(name), links)
            save_data(self)
            print('Chapters Scraped.')
            print(f"\nTotal Time Taken For Chapters:{time.time() - start_time}\n")
            return

        links = list(self.data[name]['Chapter Links'].items())
        with ThreadPoolExecutor(max_workers=8) as executor:
            executor.map(scraper.fetch_chapters, repeat(name), links)
        save_data(self)

        print('Chapters Scraped.')
        print(f"\nTotal Time Taken For Chapters:{time.time() - start_time}\n")


def run_chapter_scraper(name):
    scraper = ChapterScraper()
    scraper.find_chapters(scraper, name)
