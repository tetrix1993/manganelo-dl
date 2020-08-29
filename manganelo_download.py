from myutil.util import *
from datetime import datetime
import argparse
import json
import os

MANGANELO_DIR = 'manganelo'
STATIC_DIR = MANGANELO_DIR + '/static'
MANGA_LIST_FILEPATH = STATIC_DIR + '/manga_list.txt'
MANGA_LIST_JSON_FILEPATH = STATIC_DIR + '/data.json'
DOWNLOAD_DIR = MANGANELO_DIR + '/download'
CHAPTER_CACHE_FILE_NAME = 'cache'
CHAPTER_LIST_JSON_NAME = 'data.json'
IMAGE_LIST_JSON_NAME = 'data.json'
DOWNLOAD_HISTORY_FILE = STATIC_DIR + '/history.log'

MANGANELO_MANGA_TEMPLATE = 'https://manganelo.com/manga/%s'

# Example of url: https://rawdevart.com/comic/live-dungeon/chapter-7/

# Manga object:
# url - Name found in the url of the manga
# name - Name of the manga


def create_directories():
    if not os.path.exists(MANGANELO_DIR):
        create_directory(MANGANELO_DIR)
    if not os.path.exists(STATIC_DIR):
        create_directory(STATIC_DIR)
    if not os.path.exists(DOWNLOAD_DIR):
        create_directory(DOWNLOAD_DIR)


def read_manga_list_file():
    manga_list = []
    if not os.path.exists(MANGA_LIST_FILEPATH):
        with open(MANGA_LIST_FILEPATH, 'w+', encoding='utf-8') as f:
            pass
    else:
        with open(MANGA_LIST_FILEPATH, 'r', encoding='utf-8') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                manga = json.loads(line)
                manga_list.append(manga)
    return manga_list


def get_url_manga_name(url):
    split1 = url.split('/')
    if len(split1) == 6:
        return split1[4]
    else:
        return None


def get_chapter_url_name(url):
    split1 = url.split('/')
    if len(split1) == 6:
        return split1[5]
    else:
        return None


def get_chapter_name(soup):
    try:
        return soup.find('div', class_='panel-breadcrumb').find_all('a', class_='a-h')[2]['title']
    except:
        return None


def generate_chapter_cache(dir, chapter_name, published_date):
    chapter = {'name': chapter_name, 'datePublished': published_date}
    with open(dir, 'w+', encoding='utf-8') as f:
        json.dump(chapter, f)


def find_manga_in_manga_list(manga_list, url_name):
    """
    Returns the first item that matches url_name. Returns -1 if not found
    :param manga_list:
    :param url_name:
    :return: index of manga_list
    """
    for i in range(len(manga_list)):
        if manga_list[i]['url'] == url_name:
            return i
    return -1


def append_to_manga_list_file(id, url_name, manga_name):
    manga = {}
    manga['id'] = id
    manga['url'] = url_name
    manga['name'] = manga_name
    with open(MANGA_LIST_FILEPATH, 'a+', encoding='utf-8') as f:
        json.dump(manga, f)
        f.write('\n')


def get_manga_name(soup):
    try:
        return soup.find('div', class_='panel-breadcrumb').find_all('a', class_='a-h')[1]['title']
    except Exception as e:
        print(e)
        return None


def get_images(soup):
    images = []
    try:
        image_tags = soup.find('div', class_='container-chapter-reader').find_all('img')
        for image_tag in image_tags:
            images.append(image_tag['src'])
    except:
        pass
    return images


def generate_manga_list_json():
    manga_list = read_manga_list_file()
    if len(manga_list) == 0:
        return
    sorted_manga_list = sorted(manga_list, key=lambda i: i['name'])
    with open(MANGA_LIST_JSON_FILEPATH, 'w', encoding='utf-8') as f:
        json.dump(sorted_manga_list, f)


def generate_chapter_list_json(manga_dir):
    filelist = os.listdir(manga_dir)
    chapters = []
    for file in filelist:
        if os.path.isdir(manga_dir + '/' + file):
            chapter = {}
            cache_file = manga_dir + '/' + file + '/' + CHAPTER_CACHE_FILE_NAME
            with open(cache_file, 'r', encoding='utf-8') as f:
                chp_json = json.loads(f.readline())
                chapter['name'] = chp_json['name']
                chapter['datePublished'] = chp_json['datePublished']
            chapter['url'] = file
            chapters.append(chapter)

    if len(chapters) == 0:
        return
    sorted_chapters = sorted(chapters, key=lambda i: i['datePublished'], reverse=True)
    with open(manga_dir + '/' + CHAPTER_LIST_JSON_NAME, 'w+', encoding='utf-8') as f:
        json.dump(sorted_chapters, f)


def get_published_date(manga_url_name, chapter_url):
    try:
        if chapter_url[-1] == '/':
            chapter_url_temp = chapter_url[0:len(chapter_url) - 1]
        else:
            chapter_url_temp = chapter_url
        manga_url = MANGANELO_MANGA_TEMPLATE % manga_url_name
        soup = get_soup(manga_url)
        content = soup.find('ul', class_='row-content-chapter')
        lis = content.find_all('li')
        for li in lis:
            a_tag = li.find('a')
            if a_tag and a_tag.has_attr('href') and a_tag['href'] == chapter_url_temp:
                span_tag = li.find('span', class_='chapter-time')
                if span_tag and span_tag.has_attr('title'):
                    return datetime.strptime(span_tag['title'], '%b %d,%Y %H:%M').strftime('%Y%m%d%H%M')
    except:
        pass
    return '999999999999'


def generate_download_history(manga_url_name, chapter_url_name):
    timenow = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    with open(DOWNLOAD_HISTORY_FILE, 'a+', encoding='utf-8') as f:
        f.write(timenow + '\t' + manga_url_name + '\t' + chapter_url_name + '\n')


def generate_image_json(chapter_dir, image_filenames):
    data_json_filepath = chapter_dir + '/' + IMAGE_LIST_JSON_NAME
    with open(data_json_filepath, 'w', encoding='utf-8') as f:
        json.dump(image_filenames, f)


def process_chapter_page(index, manga_url_name, chapter_url_name, soup, url):
    manga_dir = DOWNLOAD_DIR + '/' + str(index)
    chapter_dir = manga_dir + '/' + chapter_url_name
    if os.path.exists(chapter_dir + '/001.jpg'):
        return
    chapter_name = get_chapter_name(soup)
    if chapter_name is None:
        chapter_name = chapter_url_name
    images = get_images(soup)
    published_date = get_published_date(manga_url_name, url)
    if len(images) > 0:
        if not os.path.exists(chapter_dir):
            create_directory(chapter_dir)
        filename_list = []
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
                    'Referer': url}
        for i in range(len(images)):
            image_url = images[i]
            filename = str(i + 1).zfill(3) + '.jpg'
            filepath = chapter_dir + '/' + filename
            download_image(image_url, filepath, headers=headers)
            filename_list.append(filename)
        generate_image_json(chapter_dir, filename_list)
        generate_chapter_cache(chapter_dir + '/' + CHAPTER_CACHE_FILE_NAME, chapter_name, published_date)
        generate_chapter_list_json(manga_dir)
        generate_download_history(manga_url_name, chapter_url_name)


def run(url):
    create_directories()
    manga_list = read_manga_list_file()
    manga_url_name = get_url_manga_name(url)
    chapter_url_name = get_chapter_url_name(url)
    if manga_url_name is None or chapter_url_name is None:
        print("Invalid URL")
        return
    result = find_manga_in_manga_list(manga_list, manga_url_name)

    # Process webpage
    soup = get_soup(url)

    # New manga
    if result == -1:
        manga_name = get_manga_name(soup)
        if manga_name is None:
            return
        index = len(manga_list)
        append_to_manga_list_file(index, manga_url_name, manga_name)
    else:
        index = result

    process_chapter_page(index, manga_url_name, chapter_url_name, soup, url)

    if result == -1 or not os.path.exists(MANGA_LIST_JSON_FILEPATH):
        generate_manga_list_json()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('URL', help='Input the url to the chapter')
    args = parser.parse_args()
    run(args.URL)
