from myutil.util import *
import json
import os
import math
from multiprocessing import Process
from manganelo_download import process_chapter_page
from manganelo_download import get_chapter_url_name
#from manganelo_download import get_published_date

from manganelo_download import MANGA_LIST_JSON_FILEPATH
from manganelo_download import DOWNLOAD_DIR
from manganelo_download import CHAPTER_LIST_JSON_NAME

MAX_PROCESSES = 30

MANGA_URL_TEMPLATE = 'https://manganelo.com/manga/%s'
CHAPTER_URL_TEMPLATE = 'https://manganelo.com/chapter/%s/%s'


def get_manga_list_data_json():
    manga_list = []
    if os.path.exists(MANGA_LIST_JSON_FILEPATH):
        with open(MANGA_LIST_JSON_FILEPATH, 'r', encoding='utf-8') as f:
            manga_list = json.loads(f.read())
    return manga_list


def get_last_downloaded_chapter(manga_dir):
    chapter_list = []
    with open(manga_dir + '/' + CHAPTER_LIST_JSON_NAME, 'r', encoding='utf-8') as f:
        chapter_list = json.loads(f.read())
    if len(chapter_list) > 0:
        return chapter_list[0]
    else:
        return None


def run():
    manga_list = get_manga_list_data_json()
    
    processes = []
    num_of_manga = len(manga_list)
    if MAX_PROCESSES == 0:
        return
    num_of_iterations = math.floor(num_of_manga / MAX_PROCESSES) + 1
    for i in range(num_of_iterations):
        start_index = i * MAX_PROCESSES
        end_index = min((i + 1) * MAX_PROCESSES, num_of_manga)
        for j in range(start_index, end_index):
            process = Process(target=run_process, args=(manga_list[j], ))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()


def run_process(manga):
    print('Processing %s' % manga['name'])
    latest_chapter = get_last_downloaded_chapter(DOWNLOAD_DIR + '/' + str(manga['id']))
    if latest_chapter:
        manga_url = MANGA_URL_TEMPLATE % manga['url']
        manga_soup = get_soup(manga_url)
        content = manga_soup.find('ul', class_='row-content-chapter')
        if content is None:
            return
        chapter_divs = content.find_all('li')
        for chapter_div in chapter_divs:
            chapter_url = chapter_div.find('a')['href']
            chapter_url_name = get_chapter_url_name(chapter_url)
            if chapter_url_name is None:
                print('Chapter URL name - Website format has been changed!')
                return
            if chapter_url_name == latest_chapter['url']:
                break
            chapter_soup = get_soup(chapter_url)
            published_date = datetime.strptime(chapter_div.find('span', class_='chapter-time')['title'], '%b %d,%Y %H:%M').strftime('%Y%m%d%H%M')
            if published_date < latest_chapter['datePublished']:
                break
            process_chapter_page(manga['id'], manga['url'], chapter_url_name, chapter_soup, chapter_url)
    #print('Ended processing %s' % manga['name'])


if __name__ == '__main__':
    run()
