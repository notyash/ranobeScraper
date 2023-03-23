import time
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from data import DataScraper
from data import run_data_scraper


class ChapterScraper(DataScraper):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_total_pages(driver):
        soup = BeautifulSoup(driver.page_source, 'lxml')

        try:
            totalPages = int(soup.select_one('div.pages a:last-child').get_text(strip=True))
        except AttributeError:
            try:
                totalPages = int(soup.select_one('div.pages span').get_text(strip=True))
            except AttributeError:
                totalPages = 1

        return totalPages

    def generateChapterLinks(self, name, start_url):
        options = uc.ChromeOptions()
        options.headless = True
        driver = uc.Chrome(options=options)
        driver.get(start_url)

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[style="cursor: pointer;"]'))).click()
        time.sleep(2.5)

        totalPages = self.get_total_pages(driver)

        chapters = list()
        currentPage = 0
        while currentPage < totalPages:
            soup = BeautifulSoup(driver.page_source, 'lxml')

            for element in soup.select('div.cat_block.cat_line a'):
                chapters.append(element['href'])

            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.page_next'))).click()
            currentPage += 1
            print(f"Page {currentPage} done.")

        driver.quit()
        self.data[name]['Chapter Links'] = chapters
        self.data[name]['Total Chapters'] = len(chapters)

    def get_total_chapters(self, name):
        soup = self.undetected_request(self.data[name]['Chapter Link'])
        total_chapters = int(soup.select_one('h6.title').text.split(':')[0].split(' ')[-1])
        return total_chapters

    def newChaptersFound(self, name, start_url):
        new_total_chapters = self.get_total_chapters(name)
        while True:
            if self.data[name].get('Total Chapters') is not None:
                old_total_chapters = self.data[name]['Total Chapters']
                if old_total_chapters >= new_total_chapters:
                    print('No New Chapters Found.')
                    return False, None
                else:
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

        self.data[name][f"Chapter: {chapter}"] = body

    def fetch_chapters(self, name, link):
        soup = self.make_request(link)
        links = self.data[name]['Chapter Links']
        links.reverse()
        chapter = links.index(link)
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

        # if chaptersFound is not None:
        #     with ThreadPoolExecutor(max_workers=8) as executor:
        #         executor.map(scraper.fetch_chapter_links, links)
        print(self.data[name]['Chapter Links'])
        with ThreadPoolExecutor(max_workers=8) as executor:
            executor.map(scraper.fetch_chapters, repeat(name), self.data[name]['Chapter Links'])
        scraper.save_data()

        print('Chapters Scraped.')
        print(f"\nTotal Time Taken For Chapters:{time.time() - start_time}\n")


def run_chapter_scraper(name):
    scraper = ChapterScraper()
    scraper.find_chapters(scraper, name)


if __name__ == '__main__':
    # run_novel_scraper()
    novel = run_data_scraper()
    run_chapter_scraper(novel)
