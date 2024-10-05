import time
import requests
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class NaverBlogPoster:
    def __init__(self, naver_id, naver_pw):
        self.naver_id = naver_id
        self.naver_pw = naver_pw
        self.driver = self._init_driver()
        self.cookies = {}

    def _init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 헤드리스 모드
        driver = uc.Chrome(options=chrome_options)
        return driver

    def login(self):
        self.driver.get('https://nid.naver.com/nidlogin.login')

        # ID 입력
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#id"))).send_keys(
            self.naver_id)
        # 비밀번호 입력
        self.driver.find_element(By.CSS_SELECTOR, "#pw").send_keys(self.naver_pw)
        # 로그인 버튼 클릭
        self.driver.find_element(By.CSS_SELECTOR, "#log.login").click()

        # 로그인 확인
        WebDriverWait(self.driver, 10).until(EC.url_contains('https://www.naver.com/'))

        # 쿠키 저장
        self.cookies = self.driver.get_cookies()
        print("로그인 성공")

    def post_blog(self, title, content):
        # 블로그 글쓰기 페이지로 이동
        self.driver.get('https://blog.naver.com/write')

        # 글 제목 입력
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#title"))).send_keys(
            title)

        # 글 내용 입력
        content_area = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div#se-editor")))

        # 에디터에 내용 입력
        self.driver.execute_script("arguments[0].innerHTML = arguments[1];", content_area, content)

        # 포스팅 버튼 클릭
        self.driver.find_element(By.CSS_SELECTOR, "button#publish").click()

        # 게시 완료 확인
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert.alert-success")))

        print("게시물 작성 완료")

    def quit(self):
        self.driver.quit()


# 사용 예시
if __name__ == "__main__":
    naver_id = ""  # 네이버 ID
    naver_pw = ""  # 네이버 PW

    # 블로그에 게시할 제목과 내용
    title = "내 블로그 글 제목"
    content = "<h1>안녕하세요!</h1><p>이것은 자동으로 작성된 블로그 글입니다.</p>"

    poster = NaverBlogPoster(naver_id, naver_pw)
    poster.login()
    poster.post_blog(title, content)
    poster.quit()