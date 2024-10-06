import time

import pyperclip
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By

from common.contentCrawling import combine_article_titles

# Initialize the WebDriver
driver = webdriver.Chrome()  # or webdriver.Firefox() if you use Firefox


def login_brunch(username, password):
    driver.get("https://brunch.co.kr/")

    time.sleep(0.3)
    # 로그인 버튼 클릭
    elem = driver.find_element(By.ID, "topStartBrunchButton")
    elem.click()

    # kakao login
    elem_id = driver.find_element(By.ID, "kakaoLogin")
    elem_id.click()

    time.sleep(1)
    elem_id = driver.find_element(By.ID, "loginId--1")
    elem_id.click()
    pyperclip.copy(username)
    elem_id.send_keys(Keys.CONTROL, 'v')

    # pw 복사 붙여넣기
    elem_pw = driver.find_element(By.ID, "password--2")
    elem_pw.click()
    pyperclip.copy(password)
    elem_pw.send_keys(Keys.CONTROL, 'v')
    time.sleep(0.3)

    elem_login = driver.find_element(By.CLASS_NAME, "submit")
    elem_login.click()

    time.sleep(10)

    elem_auth_agree = driver.find_element(By.CLASS_NAME, "btn_agree")
    elem_auth_agree.click()
    print("success")


def create_blog_post(title, content):
    driver.get("https://brunch.co.kr/write")
    time.sleep(2)

    title_input = driver.find_element(By.CSS_SELECTOR, '.cover_title')
    pyperclip.copy(title)
    title_input.send_keys(Keys.CONTROL, 'v')
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, '.wrap_body').click()
    content_input = driver.find_element(By.CSS_SELECTOR, '.item_type_text')
    time.sleep(0.1)
    content_input.send_keys(content)
    content_input.send_keys(Keys.CONTROL, 'v')
    file_input = driver.find_element(By.ID, 'f-file-upload-image-0')
    file_path = 'C:/workspace/python/SocailTime/SocailTime/img/36729_61606_5442.jpg'
    file_input.send_keys(file_path)

    time.sleep(10)
    driver.find_element(By.CSS_SELECTOR, '.btn_write').click()


# Main execution
if __name__ == "__main__":
    username = ""
    password = ""
    url = 'https://www.newskrw.com/news/articleView.html?idxno=36729'
    combine = combine_article_titles(url)
    title = combine.get("title")
    content = combine.get("content")

    try:
        login_brunch(username, password)
        time.sleep(1)
        create_blog_post(title, content)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
