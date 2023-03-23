from scripts.chapters import run_chapter_scraper
from scripts.data import run_data_scraper
from scripts.novels import run_novel_scraper


def main():
    run_novel_scraper()
    name = run_data_scraper()
    run_chapter_scraper(name)


if __name__ == '__main__':
    main()
