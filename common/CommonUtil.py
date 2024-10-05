import json
import os
import time
import sys
import traceback
import unicodedata

import requests
from PyQt5 import QtWidgets
from bs4 import BeautifulSoup


def log(type_, content, filename='log.json'):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write('[]')

    with open(filename, 'r+') as f:
        data = json.load(f)
        data.append({type_: [time.time(), content]})
        f.seek(0)
        json.dump(data, f)


def recently():
    result = []
    resp = requests.get("https://www.newskrw.com/").text
    soup = BeautifulSoup(resp, "html.parser")
    for div in soup.find_all("div", class_="item"):
        link = div.find("a")["href"]
        result.append("https://www.newskrw.com" + link)
        if len(result) >= 5:
            return result


def news(url):
    print(f"url : {url}")
    resp = requests.get(url).text
    soup = BeautifulSoup(resp, 'html.parser')
    heading = soup.find('meta', attrs={'name': 'title'})['content'].strip()
    subheading = soup.find('h2', class_='subheading').text.strip()

    article = soup.find("article", {"id": "article-view-content-div"})
    print(f"url : {article}")
    combined = []
    for element in article.descendants:
        if element.name == "img" or element.name == "p" or element.name == 'h2' or element.name == "div" or element.name == 'h3':
            combined.append(element)

    result = []
    for item in combined:
        if item.name == "div":
            div = item.find('div', {'data-type': 'video'})
            if div:
                iframe = div.find('iframe')
                youtube = iframe['src'].replace("https://www.youtube.com/embed/", "https://youtu.be/")
                result.append({"type": "youtube", "src": youtube})
        elif item.name == "img":
            result.append({"type": "img", "src": item["src"], "alt": unicodedata.normalize("NFKD", item["alt"])})
        elif item.name == "p" or item.name == "h2" or item.name == "h3":
            for sub_item in item.contents:
                normalized_text = unicodedata.normalize("NFKD", sub_item.text)
                if isinstance(sub_item, str):
                    if not sub_item.strip():
                        continue
                    else:
                        result.append(
                            {"type": "text", "strong": False, "text": unicodedata.normalize("NFKD", sub_item)})
                elif sub_item.name == "strong":
                    result.append({"type": "text", "strong": True, "text": normalized_text})
                else:
                    result.append({"type": "text", "strong": False, "text": normalized_text})
            if item.name == "p" or item.name == "h2" or item.name == "h3":
                result.append({"type": "end", "strong": False, 'end': True})
    return heading, subheading, result


def excepthook(exc_type, exc_value, exc_tb):
    tb_str = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
    tb_list = traceback.extract_tb(exc_tb)
    for tb in tb_list:
        tb_str += f"File '{tb.filename}', line {tb.lineno}, in {tb.name}\n"
        tb_str += f"\t{tb.line}\n"
    print(tb_str)
    log('ERROR', tb_str)


sys.excepthook = excepthook
