from bs4 import BeautifulSoup

from common.CommonUtil import fetch_page_content
from common.imgCrawling import download_images_from_class


# 기사 내용 추출
def parse_article_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # 광고성 글 삭제
    for figure in soup.find_all('figure'):
        figure.decompose()
    for ins in soup.find_all('ins'):
        ins.decompose()

    article_body = soup.find('article', id='article-view-content-div')

    if article_body:
        return article_body.decode_contents()
    else:
        print("Article body not found.")
        return None


# 많이 본 뉴스 크롤링
def parse_item_contents(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    items = soup.select('article.box-skin .item')

    extracted_data = []
    for item in items:
        link = item.find('a')['href']
        title = item.find('span', class_='auto-titles')

        if title is not None:
            extracted_data.append(("https://www.newskrw.com" + link, title))
    return extracted_data


# 기사 타이틀 크롤링
def parse_head_title(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    article_title = soup.find('h1', class_='heading')

    if article_title:
        return article_title.decode_contents()
    else:
        print("Article body not found.")
        return None


# 많이 본 뉴스 유효성 검사
def extract_links_and_titles(url):
    html_content = fetch_page_content(url)

    if html_content:
        return parse_item_contents(html_content)
    return None


# 모든 기사 유효성 검사
def extract_full_article_content(url):
    html_content = fetch_page_content(url)

    if html_content:
        return parse_article_content(html_content)
    return None


# 기사 타이틀 유효성 검사
def extract_article_title(url):
    html_content = fetch_page_content(url)

    if html_content:
        return parse_head_title(html_content)
    return None


# 통합
def combine_article_titles(url):
    html_content = fetch_page_content(url)
    download_images_from_class(url, 'grid body')

    result = {
        "title": parse_head_title(html_content),
        "content": parse_article_content(html_content),
        "link": parse_item_contents(html_content)
    }

    if html_content:
        return result


# 예제
url = 'https://www.newskrw.com/news/articleView.html?idxno=36729'
# 전체 내용 테스트
full_article_content = extract_full_article_content(url)

# 기사 테스트
item_contents = extract_links_and_titles(url)

# 제목 테스트
article_title = extract_article_title(url)
combine = combine_article_titles(url)

print(f"{combine.get('title')}")
