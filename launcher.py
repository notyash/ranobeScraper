import subprocess
import sys

import uvicorn
from fastapi import FastAPI

from scripts.chapters import run_chapter_scraper
from scripts.data import run_data_scraper
from scripts.novels import run_novel_scraper

app = FastAPI()


@app.get("/novel")
def main(title):
    p = subprocess.Popen([sys.executable, r'FlareSolverr/src/flaresolverr.py'],
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.STDOUT, )

    run_novel_scraper()
    name = run_data_scraper(title)
    if not name:
        return 'Invalid Name'
    data = run_chapter_scraper(name)
    p.terminate()
    return data


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
