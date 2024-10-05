import pyautogui
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time
import pyperclip

# Initialize the WebDriver
driver = webdriver.Chrome()  # or webdriver.Firefox() if you use Firefox


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
    title_field_xpath = '/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[1]/div[2]/section/article/div[1]/div[1]/div/div/p/span[2]'
    content_field_xpath = '/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[1]/div[2]/section/article/div[2]/div/div/div/div/p'
    publish_button_xpath = '/html/body/div[1]/div/div[1]/div/div[2]/button[1]'
    text_image_xpath = '/html/body/div[1]/div/div[3]/div/div/div[1]/div/header/div[1]/ul/li[17]/button'
    image_keyword_xpath = '/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[1]/aside/div/div[1]/input'
    first_image_xpath = '/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[1]/aside/div/div[3]/div/ul/div/li[1]/div/div[2]'

    time.sleep(3)

    write_link = driver.find_element(By.LINK_TEXT, "글쓰기")
    write_link.click()

    # Wait for the editor to load
    time.sleep(5)


    # Fill in the title
    driver.find_element(By.ID, "mainFrame").click()
    time.sleep(0.3)

    title_field = driver.find_element(By.XPATH, title_field_xpath)
    title_field.send_keys(title)

    content_field = driver.find_element(By.XPATH, content_field_xpath)
    content_field.send_keys(content)


    # Click the "Publish" button
    driver.find_element(By.CSS_SELECTOR, ".publish_btn_area__KjA2i").click()

    # Wait for the post to be published
    time.sleep(3)


# Main execution
if __name__ == "__main__":
    username = ""
    password = ""
    title = "Blog Automation Test"
    content = "This is the content of your blog post."

    try:
        login_naver(username, password)
        create_blog_post(title, content)
        print("Blog post created successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
