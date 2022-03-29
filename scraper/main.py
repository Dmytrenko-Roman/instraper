import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from config import settings


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Instagram Login:

driver.get('https://www.instagram.com/')

username_input_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="username"]')))
password_input_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]')))

username_input_field.clear()
password_input_field.clear()

username_input_field.send_keys(settings.instagram_username)
password_input_field.send_keys(settings.instagram_password)

log_in_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()

time.sleep(5)
driver.close()
driver.quit()
