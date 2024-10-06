import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from common.CommonUtil import get_root


# 이미지 다운 클레스
def download_images_from_class(url, class_name, img_folder=f"{get_root()}/img"):
    # 이미지 폴더 생성
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)

    # 페이지 문서화
    response = requests.get(url)
    if response.status_code != 200:
        print(f"크롤링 실패: {url}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # 이미지 포함된 태그 찾기
    grid_body = soup.find(class_=class_name)

    if grid_body:
        # 해당 태그내 이미지 검색
        img_tags = grid_body.find_all('img')

        for img_tag in img_tags:
            if 'src' in img_tag.attrs:
                img_url = img_tag['src']
                img_url = urljoin(url, img_url)

                # 이미지 다운 코드
                try:
                    img_response = requests.get(img_url)
                    img_name = os.path.join(img_folder, img_url.split('/')[-1])

                    with open(img_name, 'wb') as f:
                        f.write(img_response.content)

                    print(f'다운로드 : {img_name}')
                except Exception as e:
                    print(f'다운 실패 {img_url}: {e}')
            else:
                print('이미지 없음')
    else:
        print(f'Class "{class_name}" 해당 태그 못찾음')


url = 'https://www.newskrw.com/news/articleView.html?idxno=36729'
class_name = 'grid body'
download_images_from_class(url, 'grid body')
