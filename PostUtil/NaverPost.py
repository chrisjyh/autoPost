import datetime
import html
import json
import random
import string
import time
import unicodedata
import uuid
from io import BytesIO

import pyperclip
import requests
import undetected_chromedriver as uc
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from common.CommonUtil import log, news, recently

cookies = {}
cookies_pin = {}

class NaverPost:
    def __init__(self, id_, pw):
        self.id_ = id_
        self.pw = pw

    def _naver_login(self):
        global cookies

        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # driver = uc.Chrome(options=chrome_options)
        driver = webdriver.Chrome()
        driver.get('https://nid.naver.com/nidlogin.login')

        time.sleep(0.3)
        # 로그인 버튼 클릭
        elem = driver.find_element(By.CSS_SELECTOR, ".btn_login")
        elem.click()

        # id 복사 붙여넣기
        elem_id = driver.find_element(By.ID, "id")
        elem_id.click()
        pyperclip.copy(self.id_)
        elem_id.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)

        # pw 복사 붙여넣기
        elem_pw = driver.find_element(By.ID, "pw")
        elem_pw.click()
        pyperclip.copy(self.pw)
        elem_pw.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)

        # 로그인 버튼 클릭
        elem.click()
        return driver



    def _analyze_links(self, url, type):
        token = requests.get(
            f'https://blog.naver.com/PostWriteFormSeOptions.naver?blogId={self.id_}',
            cookies=cookies
        ).json()['result']['token']
        headers = {
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'pragma': 'no-cache', 'se-authorization': token,
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'accept': 'application/json',
            'sec-ch-ua-platform': '"Windows"',
            'origin': 'https://blog.naver.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://blog.naver.com/PostWriteForm.naver',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        resp = requests.get(
            "https://platform.editor.naver.com/api/blogpc001/v1/oglink",
            params={'url': url},
            cookies=cookies,
            headers=headers
        ).json()

        if type == "youtube":
            return resp['oembed']['html'], resp['oembed']['width'], resp['oembed']['height'], resp['oembed']['authorName'], resp['oembed']['authorUrl'], resp['oembed']['thumbnailUrl'], resp['oembed']['thumbnailWidth'], resp['oembed']['thumbnailHeight'], resp["oglink"]["summary"]["title"], resp["oglink"]["summary"]["description"], resp['oembedSign']
        if type == "img":
            return resp['image']['width'], resp['image']['height']
        if type == "news":
            return resp["oglink"]["summary"]['image']['width'], resp["oglink"]["summary"]['image']['height'], resp["oglink"]["summary"]["title"], resp["oglink"]["summary"]["description"], resp["oglink"]["summary"]["image"]["url"], resp['oglinkSign']

    def _preprocess_data(self, data):
        output_list = []
        sentence = {}

        for text_dict in data:
            if 'end' in text_dict:
                if not sentence:
                    continue
                output_list.append({'type': 'text', 'text': sentence})
                sentence = {}
                continue
            try:
                text = unicodedata.normalize("NFC", text_dict['text'])
            except:
                output_list.append(text_dict)
                continue
            if not text:
                continue
            is_strong = False
            if 'strong' in text_dict and text_dict['strong']:
                is_strong = True
            sentence[text] = is_strong
        return output_list

    def __blog_payload(self, news):
        title = news[0]
        subtitle = news[1]
        output_list = self._preprocess_data(news[2])
        title = json.dumps({"id": f"SE-{uuid.uuid4()}", "layout": "default", "title": [{"id": f"SE-{uuid.uuid4()}", "nodes": [{"id": f"SE-{uuid.uuid4()}", "value": title.replace('"', '\"'), "@ctype": "textNode"}], "@ctype": "paragraph"}], "subTitle": None, "align": "left", "@ctype": "documentTitle"}, ensure_ascii=False)
        subtitle = json.dumps({"id": f"SE-{uuid.uuid4()}", "layout": "quotation_line", "value": [{"id": f"SE-{uuid.uuid4()}", "nodes": [{"id": f"SE-{uuid.uuid4()}", "value": subtitle.replace('"', '\"'), "@ctype": "textNode"}], "@ctype": "paragraph"}], "source": None, "@ctype": "quotation"}, ensure_ascii=False)
        result = [title, subtitle]
        text_format = {"id": f"SE-{uuid.uuid4()}", "layout": "default", "value": [], "@ctype": "text"}
        for element in output_list:
            if element['type'] == 'text':
                text = {"id": f"SE-{uuid.uuid4()}", "nodes": [], "@ctype": "paragraph"}
                for i in element['text']:
                    if element['text'][i]:
                        text["nodes"].append({"id": f"SE-{uuid.uuid4()}", "value": i.replace('"', '\"').replace("\'", "'"), "style": {"bold": True, "@ctype": "nodeStyle"}, "@ctype": "textNode"})
                    else:
                        text["nodes"].append({"id": f"SE-{uuid.uuid4()}", "value": i.replace('"', '\"').replace("\'", "'"), "@ctype": "textNode"})
                text["nodes"].append({"id": f"SE-{uuid.uuid4()}", "value": "", "@ctype": "textNode"})
                text_format['value'].append(text)
                result.append(json.dumps(text_format, ensure_ascii=False))
                text_format = {"id": f"SE-{uuid.uuid4()}", "layout": "default", "value": [], "@ctype": "text"}
            elif element['type'] == 'img':
                img_size = self._analyze_links(element['src'], 'img')
                result.append(json.dumps({"id": f"SE-{uuid.uuid4()}", "layout": "default", "src": element['src'], "internalResource": False, "represent": False, "domain": "https://blogfiles.pstatic.net", "fileSize": 0, "width": img_size[0], "widthPercentage": 0, "height": img_size[1], "originalWidth": img_size[0], "originalHeight": img_size[1], "caption": [{"id": f"SE-{uuid.uuid4()}", "nodes": [{"id": f"SE-{uuid.uuid4()}", "value": element['alt'].replace('"', '\"'), "@ctype": "textNode"}], "@ctype": "paragraph"}], "format": "normal", "displayFormat": "normal", "imageLoaded": True, "contentMode": "normal", "origin": {"srcFrom": "copyUrl", "@ctype": "imageOrigin"}, "@ctype": "image"}, ensure_ascii=False))
            elif element['type'] == 'youtube':
                youtube = self._analyze_links(element['src'], 'youtube')
                result.append(json.dumps(
                    {"id": f"SE-{uuid.uuid4()}", "layout": "default", "type": "video", "version": "1.0", "html": youtube[0], "originalWidth": youtube[1], "originalHeight": youtube[2], "authorName": youtube[3], "authorUrl": youtube[4], "providerName": "YouTube", "providerUrl": "https://www.youtube.com/", "thumbnailUrl": youtube[5], "thumbnailWidth": youtube[6], "thumbnailHeight": youtube[7], "title": youtube[8], "description": youtube[9], "inputUrl": element['src'], "contentMode": "fit",
                     "oembedSign": youtube[10], "@ctype": "oembed"}, ensure_ascii=False))

        result.append(json.dumps({"id": f"SE-{uuid.uuid4()}", "layout": "quotation_bubble", "value": [{"id": f"SE-{uuid.uuid4()}", "nodes": [{"id": f"SE-{uuid.uuid4()}", "value": "뉴스클립 많이 본 기사", "@ctype": "textNode"}], "@ctype": "paragraph"}], "source": None, "@ctype": "quotation"}, ensure_ascii=False))
        for link in recently():
            info = self._analyze_links(link, 'news')
            result.append(json.dumps({"id": f"SE-{uuid.uuid4()}", "layout": "default", "value": [{"id": f"SE-{uuid.uuid4()}", "nodes": [{"id": f"SE-{uuid.uuid4()}", "value": link, "link": {"url": link, "@ctype": "urlLink"}, "@ctype": "textNode"}], "style": {"align": "center", "@ctype": "paragraphStyle"}, "@ctype": "paragraph"}], "@ctype": "text"}, ensure_ascii=False))
            result.append(json.dumps({"id": f"SE-{uuid.uuid4()}", "layout": "large_image", "align": "center", "title": info[2], "domain": "www.newskrw.com", "link": link, "thumbnail": {"src": info[4], "width": info[0], "height": info[1], "@ctype": "thumbnail"}, "description": info[3], "video": False, "oglinkSign": info[-1], "@ctype": "oglink"}, ensure_ascii=False))
            result.append(json.dumps({"id": f"SE-{uuid.uuid4()}", "layout": "default", "value": [{"id": f"SE-{uuid.uuid4()}", "nodes": [{"id": f"SE-{uuid.uuid4()}", "value": "", "@ctype": "textNode"}], "style": {"align": "center", "@ctype": "paragraphStyle"}, "@ctype": "paragraph"}], "@ctype": "text"}, ensure_ascii=False))
        documentId = '''{"documentId":"","document":{"version":"2.6.0","theme":"default","language":"ko-KR","components":[''' + ','.join(result) + ']}}'
        return documentId

    def _post_payload(self, news):
        title = news[0]
        subtitle = news[1]
        output_list = self._preprocess_data(news[2])

        timestamp = int(time.time() * 1000)
        headers = {'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"', 'accept': 'application/json, text/javascript, */*; q=0.01', 'x-requested-with': 'XMLHttpRequest', 'sec-ch-ua-mobile': '?0', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://post.editor.naver.com/editor', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'}
        tempId = requests.get(f"https://post.editor.naver.com/temporary/key.json?serviceId=post&userId={self.id_}&_={timestamp}", params={'serviceId': 'post', 'userId': self.id_, '_': str(int(time.time() * 1000))}, cookies=cookies, headers=headers).json()['result']['tempId']

        delta = datetime.timedelta(hours=9)
        utc_now = datetime.datetime.utcnow()
        kst_now = utc_now + delta
        date = kst_now.strftime('%Y-%m-%dT%H:%M:%S+09:00')
        timestamp = int(time.time() * 1000)

        components = [{"title": title, "subtitle": "", "publishDate": 0, "background": {"@ctype": "background", "color": ""}, "@ctype": "documentTitle", "layout": "default", "isFocused": False, "componentStyle": {"@ctype": "componentStyle", "fontFamily": "nanumgothic", "fontSize": "D2", "align": "left"}, "compId": f"documentTitle_{random.randint(10000000, 600000000)}{timestamp - random.randint(1000, 2000)}", "focusComp": False},
                      {"value": "", "hasDropCap": False, "@ctype": "paragraph", "layout": "default", "isFocused": False, "componentStyle": {"@ctype": "componentStyle", "fontFamily": "nanumgothic", "fontSize": "T3", "align": "left", "lineHeight": ""}, "compId": f"paragraph_{random.randint(10000000, 600000000)}{timestamp - random.randint(1000, 2000)}", "focusComp": False},
                      {"value": subtitle, "@ctype": "quotation", "layout": "quotation_line", "isFocused": False, "componentStyle": {"@ctype": "componentStyle", "fontSize": "T3"}, "compId": f"quotation_{random.randint(10000000, 600000000)}{timestamp - random.randint(1000, 2000)}", "focusComp": False}]
        for element in output_list:
            if element['type'] == 'text':
                components.append({"value": ''.join([f"<b>{key}</b>" if value else key for key, value in element['text'].items()]), "hasDropCap": False, "@ctype": "paragraph", "layout": "default", "isFocused": False, "componentStyle": {"@ctype": "componentStyle", "fontFamily": "nanumgothic", "fontSize": "T3", "align": "left", "lineHeight": ""}, "compId": f"paragraph_{random.randint(10000000, 600000000)}{timestamp - random.randint(1000, 2000)}", "focusComp": False}, )
            elif element['type'] == 'img':
                response = requests.get(element['src'])
                img = Image.open(BytesIO(response.content))
                img.save('image.png', 'PNG')
                with open('image.png', 'rb') as f:
                    file_content = f.read()
                multipart_data = MultipartEncoder(fields={'image': ('image.png', file_content, 'image/png')}, boundary='----WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16)))
                headers = {'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"', 'accept': 'application/json, text/javascript, */*; q=0.01', 'x-requested-with': 'XMLHttpRequest', 'sec-ch-ua-mobile': '?0', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://post.editor.naver.com/editor/canvas?serviceId=post&deviceType=desktop&docType=normal', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'}
                sessionKey = requests.get(f"https://post.editor.naver.com/PhotoUploader/SessionKey.json?uploaderType=simple&userId={self.id_}&serviceId=post&_={int(time.time() * 1000)}", cookies=cookies, headers=headers).json()['result']['sessionKey']
                resp = requests.post(f"https://ecommerce.upphoto.naver.com/{sessionKey}/simpleUpload/0?userId={self.id_}&extractExif=false&extractAnimatedCnt=true&autorotate=true&extractDominantColor=false&type=", headers={'Content-type': multipart_data.content_type}, data=multipart_data, cookies=cookies).text
                components.append({"src": f"https://post-phinf.pstatic.net/{resp.split('<url>')[1].split('<')[0]}?type=w1200", "width": int(resp.split('<width>')[1].split('<')[0]), "height": int(resp.split('<height>')[1].split('<')[0]), "originalWidth": int(resp.split('<width>')[1].split('<')[0]), "originalHeight": int(resp.split('<height>')[1].split('<')[0]), "alt": resp.split('<fileName>')[1].split('<')[0], "caption": element['alt'], "captionLink": "", "path": resp.split('<thumbnail>')[1].split('<')[0], "domain": "https://post-phinf.pstatic.net", "uploadedLocal": True, "offsetCenterXRatio": 0, "offsetCenterYRatio": 0, "backgroundPositionX": "50%", "backgroundPositionY": "50%", "fileSize": resp.split('<fileSize>')[1].split('<')[0], "represent": True, "fileName": resp.split('<fileName>')[1].split('<')[0], "animationGIF": False, "generationFormat": "normal", "displayFormat": "normal", "@ctype": "image", "layout": "default", "isFocused": False,
                                   "componentStyle": {"@ctype": "componentStyle", "align": "justify"}, "compId": f"image_{random.randint(10000000, 600000000)}{timestamp - random.randint(1000, 2000)}", "focusComp": False})
            elif element['type'] == 'youtube':
                resp = requests.get(f"https://ogcrawler.editor.naver.com/crawler.json?url={element['src']}&serviceId=post&userId=&_=").json()
                components.append({"@ctype": "oglink", "layout": "og_bSize", "title": html.unescape(resp['summary']['title']), "link": element['src'], "componentStyle": {"@ctype": "componentStyle", "align": "left"}, "desc": html.unescape(resp['summary']['description']), "isVideo": True, "domain": "youtu.be", "thumbnail": {"@ctype": "thumbnail", "src": resp['summary']['image']['url'], "width": resp['summary']['image']['width'], "height": resp['summary']['image']['height']}, "isFocused": False, "compId": f"oglink_{random.randint(10000000, 600000000)}{timestamp - random.randint(1000, 2000)}", "focusComp": False})
        components.append({"value": "뉴스클립 많이 본 기사", "@ctype": "quotation", "layout": "quotation_bubble", "isFocused": False, "componentStyle": {"@ctype": "componentStyle", "fontSize": "T3"}, "compId": f"quotation_{random.randint(10000000, 600000000)}{timestamp - random.randint(1000, 2000)}", "focusComp": False})
        for link in recently():
            resp = requests.get(f"https://ogcrawler.editor.naver.com/crawler.json?url={link}&serviceId=post&userId=&_=").json()
            components.append({"value": f"<a href=\"{link}\" target=\"_blank\" class=\"se_link\">{link}</a>", "hasDropCap": False, "@ctype": "paragraph", "layout": "default", "isFocused": False, "componentStyle": {"@ctype": "componentStyle", "fontFamily": "nanumgothic", "fontSize": "T3", "align": "center", "lineHeight": ""}, "compId": f"paragraph_{random.randint(10000000, 600000000)}{timestamp - random.randint(1000, 2000)}", "focusComp": False})
            components.append({"@ctype": "oglink", "layout": "og_bSize", "title": html.unescape(resp['summary']['title']).replace('"', '\"'), "link": link, "componentStyle": {"@ctype": "componentStyle", "align": "center"}, "desc": html.unescape(resp['summary']['description']), "isVideo": False, "domain": "www.newskrw.com", "thumbnail": {"@ctype": "thumbnail", "src": resp['summary']['image']['url'], "width": resp['summary']['image']['width'], "height": resp['summary']['image']['height']}, "isFocused": False, "compId": f"oglink_{random.randint(10000000, 600000000)}{timestamp - random.randint(1000, 2000)}", "focusComp": False})
            components.append({"value": "<span><br></span><span></span>", "hasDropCap": False, "@ctype": "paragraph", "layout": "default", "isFocused": False, "componentStyle": {"@ctype": "componentStyle", "fontFamily": "nanumgothic", "fontSize": "T3", "align": "center", "lineHeight": ""}, "compId": f"paragraph_{random.randint(10000000, 600000000)}{timestamp - random.randint(1000, 2000)}", "focusComp": False})

        payload = {"serviceId": "post", "document": {"docType": "normal", "title": title, "thumbnail": "", "theme": "default", "author": "", "publishDate": date, "documentStyle": {"@ctype": "documentStyle"}, "representativeLocation": None, "scrapDocData": None, "components": components}, "docType": "normal", "publishMeta": {"title": "", "templateType": "UGC_SIMPLE", "volumeNo": -1, "seriesNo": 0, "openType": 0, "searchNotAllowed": 0, "volumeAuthorComment": "", "reserveDate": "", "blogPublish": False, "facebookPublish": False, "twitterPublish": False, "blogCategoryNo": None, "cloudTags": [], "status": "", "categoryNo": 0, "masterYn": True, "docTemplateType": "", "termsSynonym": "", "termsLastUpdateDate": "", "cmtType": 0, "cmtOrderType": 0, "@service": "post"}, "tempDocumentId": str(tempId)}
        return payload

    def blog(self, articles):
        print("진입")
        driver = self._naver_login()




    def post(self, driver):
        driver.get("https://blog.naver.com/")
        time.sleep(5)
        try:
            # Click the "글쓰기" link using link text
            write_link = driver.find_element(By.LINK_TEXT, "글쓰기")
            write_link.click()

            # Alternatively, you could use the CSS selector:
            # write_link = driver.find_element(By.CSS_SELECTOR, "a.item[alt='글쓰기']")
            # write_link.click()

            print("Clicked on '글쓰기' link successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")


