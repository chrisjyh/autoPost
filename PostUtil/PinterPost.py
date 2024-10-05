import time
import unicodedata

import requests
import undetected_chromedriver as uc
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common.CommonUtil import log, news

cookies = {}
cookies_pin = {}

class PinterPost:
    def __init__(self, id_, pw):
        self.id_ = id_
        self.pw = pw

    def _pinterest_login(self):
        global cookies_pin
        if "full_name" in requests.get("https://www.pinterest.co.kr/resource/AdvancedTypeaheadResource/get/?source_url=%2F&data=%7B%22options%22%3A%7B%22term%22%3A%22%22%2C%22pin_scope%22%3A%22pins%22%7D%2C%22context%22%3A%7B%7D%7D&_=", cookies=cookies_pin).text:
            return True

        chrome_options = Options()
        chrome_options.add_argument('--headless')

        driver = uc.Chrome(options=chrome_options)
        driver.get('https://www.pinterest.co.kr/')
        action = ActionChains(driver)

        element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#fullpage-wrapper > div.section.fp-section.active.fp-table.fp-completely > div > div > div.QLY._he.zI7.iyn.Hsu > div > div.Eqh.KS5.hs0.un8.C9i.TB_ > div.wc1.zI7.iyn.Hsu > button")))
        time.sleep(0.3)
        action.click(element).perform()
        element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/div/div/div/div/div/div[4]/div[1]/div[1]/div/button")))
        time.sleep(0.3)
        action.click(element).perform()
        WebDriverWait(driver, 5).until(EC.new_window_is_opened)
        time.sleep(0.3)
        facebook = driver.window_handles[1]
        driver.switch_to.window(facebook)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#email")))
        time.sleep(0.3)
        driver.execute_script(f"document.querySelector('input[id=\"email\"]').setAttribute('value', '{self.id_}')")
        time.sleep(0.1)
        driver.execute_script(f"document.querySelector('input[id=\"pass\"]').setAttribute('value', '{self.pw}')")
        time.sleep(0.3)
        driver.find_element(By.XPATH, "/html/body/div/div[2]/div[1]/form/div/div[3]/label[2]/input").click()
        driver.switch_to.window(driver.window_handles[0])
        start = time.time()
        while time.time() - start <= 300:
            if "계정 및" in driver.page_source:
                driver_cookies = driver.get_cookies()
                for cookie in driver_cookies:
                    cookies_pin[cookie['name']] = cookie['value']
                driver.quit()
                return True
            time.sleep(0.1)
        else:
            log("로그인 실패", "핀터레스트")
            driver.quit()
            return False

    def pinterest(self, articles):
        if not self._pinterest_login():
            return
        resp = requests.get("https://www.pinterest.co.kr/resource/AdvancedTypeaheadResource/get/?source_url=%2F&data=%7B%22options%22%3A%7B%22term%22%3A%22%22%2C%22pin_scope%22%3A%22pins%22%7D%2C%22context%22%3A%7B%7D%7D&_=", cookies=cookies_pin).json()
        experiment_hash = resp['client_context']['experiment_hash']
        username = resp['client_context']['user']['username']
        id_ = requests.get('https://www.pinterest.co.kr/resource/BoardsResource/get/?source_url=/pin-builder/&data={"options":{"page_size":1,"privacy_filter":"all","sort":"last_pinned_to","username":"%s"},"context":{}}&_=' % (username), cookies=cookies).json()['resource_response']['data'][0]['id']
        for article in articles:
            try:
                result = news(article)
                text_list = [item['text'] for item in result[2] if item['type'] == 'text']
                text = ''.join(text_list).replace('\n\n', '')[:500]
                title = result[0][:100]
                img_urls = [i['url'] for i in requests.get('https://www.pinterest.co.kr/resource/FindPinImagesResource/get/?source_url=/pin-builder/&data={"options":{"url":"%s","source":"pin_create","appendItems":false,"followRedirects":true,"scrapeMetric":"www_url_scrape"},"context":{}}&_=' % (article)).json()['resource_response']['data']['items']][:10]
                for img_url in img_urls:
                    headers = {'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"', 'x-pinterest-appstate': 'active', 'x-pinterest-pws-handler': 'www/pin-builder.js', 'sec-ch-ua-platform-version': '"15.0.0"', 'x-requested-with': 'XMLHttpRequest', 'sec-ch-ua-full-version-list': '"Chromium";v="112.0.5615.121", "Google Chrome";v="112.0.5615.121", "Not:A-Brand";v="99.0.0.0"', 'x-csrftoken': cookies_pin['csrftoken'], 'sec-ch-ua-model': '""', 'sec-ch-ua-platform': '"Windows"', 'x-app-version': 'c139604', 'x-pinterest-experimenthash': experiment_hash, 'sec-ch-ua-mobile': '?0', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36', 'content-type': 'application/x-www-form-urlencoded', 'accept': 'application/json, text/javascript, */*, q=0.01', 'x-pinterest-source-url': '/pin-builder/', 'origin': 'https://www.pinterest.co.kr', 'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'cors',
                               'sec-fetch-dest': 'empty', 'referer': 'https://www.pinterest.co.kr/', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'}
                    payload = {'source_url': '/pin-builder/', 'data': '{"options":{"field_set_key":"create_success","skip_pin_create_log":true,"board_id":"%s","description":"%s","link":"%s","title":"%s","image_url":"%s","method":"scraped","scrape_metric":{"source":"www_url_scrape"},"user_mention_tags":[]},"context":{}}' % (id_, unicodedata.normalize('NFKC', text).replace('"', r'\"'), article, unicodedata.normalize('NFKC', title).replace('"', r'\"'), img_url)}
                    requests.post('https://www.pinterest.co.kr/resource/PinResource/create/', headers=headers, cookies=cookies_pin, data=payload)
            except:
                log('핀터레스트 업로드 실패', article)
