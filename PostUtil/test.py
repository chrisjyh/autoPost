import time

import pyperclip
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()


# 네이버 로그인
def login_naver(username, password):
    driver.get("https://nid.naver.com/nidlogin.login")

    time.sleep(0.3)
    # 로그인 버튼 클릭
    elem = driver.find_element(By.CSS_SELECTOR, ".btn_login")
    elem.click()

    # id 복사 붙여넣기
    elem_id = driver.find_element(By.ID, "id")
    elem_id.click()
    pyperclip.copy(username)
    elem_id.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)

    # pw 복사 붙여넣기
    elem_pw = driver.find_element(By.ID, "pw")
    elem_pw.click()
    pyperclip.copy(password)
    elem_pw.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)

    # 로그인 버튼 클릭
    elem.click()

    time.sleep(2)

    print("success")


def create_blog_post(title, content):
    driver.get("https://blog.naver.com/")
    time.sleep(2)

    write_link = driver.find_element(By.LINK_TEXT, "글쓰기")
    write_link.click()
    time.sleep(3)

    try:
        # iframe 찾기
        iframe = driver.find_element(By.ID, 'mainFrame')

        # iframe으로 전환
        driver.switch_to.frame(iframe)

        # iframe에 포커스 맞추기
        driver.execute_script("document.querySelector('#mainFrame').focus();")

        # 필요한 추가 작업을 수행할 수 있습니다.
        # 예를 들어, 특정 요소를 클릭하거나 텍스트 입력 등을 할 수 있습니다.

    except Exception as e:
        print("iframe을 찾거나 전환하는 데 오류가 발생했습니다:", e)


# Main execution
if __name__ == "__main__":
    username = ""
    password = ""
    title = "Blog Automation Test"
    content = "This is the content of your blog post."

    try:
        login_naver(username, password)
        create_blog_post(title, content)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
