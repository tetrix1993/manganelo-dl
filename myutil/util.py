import requests
import urllib.request
import os
from datetime import datetime
from bs4 import BeautifulSoup as bs

#Need install requests: run "pip install requests"

def get_response(url):
    response = ""
    try:
        response = str(urllib.request.urlopen(url).read())
    except Exception as e:
        print(e)
    return response

def get_soup(url, headers=None):
    if headers == None:
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    try:
        result = requests.get(url, headers=headers)
        return bs(result.text, 'html.parser')
    except Exception as e:
        print(e)
    return ""

def get_response_with_header(url, headers=None, charset=None):
    response = ""
    headers = {}
    if not headers:
        headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    else:
        headers = headers
    if charset:
        headers['Content-Type'] = 'text/html; charset=' + charset
    try:
        result = requests.get(url, headers=headers)
        if charset:
            response = str(result.content.decode(charset))
        else:
            response = str(result.content.decode())
    except Exception as e:
        print(e)
    return response

def post_response(url, headers=None, data=None):
    response = ""
    if headers == None:
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    try:
        result = requests.post(url, headers=headers, data=data)
        response = str(result.content.decode())
    except Exception as e:
        print(e)
    return response

def is_file_exists(filepath):
    return os.path.isfile(filepath)
    
def is_dir_exists(filepath):
    return os.path.isdir(filepath)

def download_image_with_split(first_split, product_id, save_folder, file_format):
    for i in range(len(first_split)):
        if i == 0:
            continue
        image_url = first_split[i].split("\"")[0]
        filepath = save_folder + "/" + str(product_id)
        if (len(first_split) > 2):
            filepath += "_" + str(i).zfill(2)
        if "." in file_format:
            filepath += file_format
        else:
            filepath += "." + file_format
        download_image(image_url, filepath)

def download_image(url, filepath, print_error_message=True, headers=None):
    # Check local directory if the file exists
    if (is_file_exists(filepath)):
        print("File exists: " + filepath)
        return False
        
    # Download image:
    try:
        if headers == None:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(filepath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            print("Downloaded " + url)
            return True
        else:
            with requests.get(url, stream=True, headers=headers) as r:
                r.raise_for_status()
                with open(filepath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            print("Downloaded " + url)
            return True
    except Exception as e:
        if print_error_message:
            print("Failed to download " + url + ' - ' + str(e))
        return False

def create_directory(filepath):
    # If directory exists
    if not os.path.exists(filepath):
        os.makedirs(filepath)

def read_input_by_line(filepath):
    if not is_file_exists(filepath):
        print(filepath + " not found")
        return []
    results = []
    f = open(filepath, "r")
    for line in f:
        results.append(line.strip())
    return results

def to_valid_name(name):
    return name.replace(' ','_').replace(':','').replace('\\','_').replace('/','_').replace('*','') \
        .replace('"',"'").replace('?','').replace('<','').replace('>','').replace('|','')

def get_today_date():
    return datetime.today().strftime('%Y%m%d')

def get_today_datetime(second=False):
    if second:
        return datetime.today().strftime('%Y%m%d%H%M%S')
    else:
        return datetime.today().strftime('%Y%m%d%H%M')

def get_numbers_from_expression(expr):
    results = []
    
    valid_chars = "0123456789-,"
    
    for i in expr:
        if i not in valid_chars:
            return []
    
    split1 = expr.split(",")
    for ex in split1:
        split2 = ex.split("-")
        if len(split2) == 1:
            try:
                results.append(int(split2[0]))
            except:
                return []
        elif len(split2) == 2:
            try:
                first_num = int(split2[0])
                last_num = int(split2[1])
                for j in range(first_num, last_num + 1, 1):
                    results.append(j)
            except:
                return []
        else:
            return []
    return results
