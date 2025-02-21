from seleniumbase import Driver
import time
import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("login")
PASSWORD = os.getenv("pass")

driver = Driver(uc=True)
url = "https://keyauth.cc/login"
driver.uc_open_with_reconnect(url, 10)
driver.uc_gui_click_captcha()

time.sleep(5)

username_xpath = "/html/body/section/div/div[2]/div/form/div[3]/input"
password_xpath = "/html/body/section/div/div[2]/div/form/div[4]/input"
login_button_xpath = "/html/body/section/div/div[2]/div/form/button"

driver.find_element("xpath", username_xpath).send_keys(USERNAME)
driver.find_element("xpath", password_xpath).send_keys(PASSWORD)

time.sleep(2)

driver.find_element("xpath", login_button_xpath).click()

time.sleep(100)

driver.quit()
