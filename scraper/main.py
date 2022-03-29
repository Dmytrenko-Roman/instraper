import time
from typing import NoReturn

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from config import settings


def set_up_driver() -> webdriver:
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
	driver.get('https://www.instagram.com/')
	return driver

def not_now_dismiss(driver: webdriver) -> WebDriverWait:
	return WebDriverWait(driver, 10).until(
		EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Не зараз")]'))
	).click()

def instagram_scraping(driver: webdriver) -> NoReturn:
	# Instagram Login:

	username_input_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="username"]')))
	password_input_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]')))

	username_input_field.clear()
	password_input_field.clear()

	username_input_field.send_keys(settings.instagram_username)
	password_input_field.send_keys(settings.instagram_password)
	
	log_in_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()

	# Dismissing pop up messages:

	not_now_save_data_button = not_now_dismiss(driver)
	not_now_notification_button = not_now_dismiss(driver)


if __name__ == '__main__':
	driver = set_up_driver()
	instagram_scraping(driver)
