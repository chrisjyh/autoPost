import json
import os
import time

import requests
from bs4 import BeautifulSoup

# img 폴더 내에 있는 파일 이름 전부 가져오기


# 루트 주소 얻기
def get_root():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    return parent_dir

# 로그
def log(type_, content, filename='log.json'):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write('[]')

    with open(filename, 'r+') as f:
        data = json.load(f)
        data.append({type_: [time.time(), content]})
        f.seek(0)
        json.dump(data, f)


# html 태그 제거 함수
def remove_html_tags(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    return soup.get_text(strip=True)


# url 유효성 검사
def fetch_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None
