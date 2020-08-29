# Manganelo Downloader
Download manga/comic from [Manganelo](https://manganelo.com/) and view it in a simple website that runs on your machine.

## Introduction
Manganelo Downloader allows you to download manga/comic from [Manganelo](https://manganelo.com/). The program is written in Python 3.0. A simple UI for viewing the manga/comic downloaded is available as an HTML page which can be run on the local machine.\
![image001.jpg](/images/image001.jpg)

## Setting Up
1. Download and install the latest version of [Python](https://www.python.org/downloads/)
2. When installing Python, make sure to check 'Add Python 3.X to PATH':\
![win_installer.png](/images/win_installer.png)
3. Open the Command Prompt (for Windows) or Terminal (for MacOS).
4. Run the following commands:
```
pip install requests
pip install bs4
```

## Running The Program
### Download New Manga/Comic
This section explains how to download a new manga/comic series for the first time.
1. Using the Command Prompt (Terminal for MacOS), change to the directory to where the file `manganelo_download.py` is located.
    1. For example, if the file is located at `D:/manganelo-dl` on your machine, enter `cd "D:/manganelo-dl"` to change to that directory.
2. Run the following command: `python manganelo_download.py <URL>`
    1. Where `<URL>` is the URL of the very first chapter that manga you want to download.
    2. Example: `python manganelo_download.py https://manganelo.com/chapter/cn919171/chapter_1`
    3. This will download that chapter for the series.
    4. Note: If you want to download subsequent chapters to the latest, use `manganelo_update.py` instead which is explained in the next section.

### Update Manga/Comic
Manganelo Downloader allows one to check whether there is/are new chapter(s) uploaded onto the website for the manga/comic series you have downloaded in the earlier section. You may run this command: `python manganelo_update.py` to check whether there are new chapter(s), which will download to your machine when available.
1. Using the Command Prompt (Terminal for MacOS), change to the directory to where the file `manganelo_update.py` is located.
2. Run the following command: `python manganelo_update.py`
3. The program will check for latest chapter and will download them if available (you will see download messages if available).
4. Note: This update script will never download older chapters that are currently downloaded on your machine. For example, if you only downloaded Chapter 3 of the manga, it will not download Chapter 1 and 2, but will download subsequent chapters (e.g. Chapter 4) if available. If you want to download earlier chapters, you must use `python manganelo_download.py <URL>` as explained in the above section.

### UI Viewer
The UI can be viewed on your browser by running a server on your local machine. You must download at least one manga/comic to proceed with this section.
1. Using the Command Prompt (Terminal for MacOS), change to the directory to where the file `manganelo_download.py` is located.
2. Change directory to the `manganelo` folder (i.e. `cd manganelo`)
3. Run the command `python -m http.server` to run a server on your local machine at port 8000.
    1. You may specify the port number using the command: `python -m http.server [PORT]` (e.g. `python -m http.server 12345`)
4. Open a browser of your choice (e.g. Google Chrome) and in the address bar, enter the URL: `localhost:8000` (if you specify the port number `12345`, the URL will be `localhost:12345`)
5. You may select the series and chapter:\
![image002.jpg](/images/image002.jpg)\
![image003.jpg](/images/image003.jpg)
6. The chapters are sorted in the order where the chapters are uploaded to the website, latest at the top. So it is possible to have chapters to be out of order, especially if multiple chapters are uploaded at the same time (e.g. Chapter 3 is uploaded first before Chapter 1, Chapter 1 to 20 is uploaded at the same time etc.)
