from seleniumbase import Driver
import time

driver = Driver(uc=True)
url = "https://keyauth.cc/login"
driver.uc_open_with_reconnect(url, 10)
driver.uc_gui_click_captcha()
time.sleep(60)