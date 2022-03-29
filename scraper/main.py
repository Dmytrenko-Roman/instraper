import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Instagram Login:

driver.get('https://www.instagram.com/')

username_input_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="username"]')))
password_input_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]')))
log_in_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()

username_input_field.clear()
password_input_field.clear()

username_input_field.send_keys('hoggerdogger')
password_input_field.send_keys('hoggerdogger')

time.sleep(5)
driver.close()
driver.quit()
