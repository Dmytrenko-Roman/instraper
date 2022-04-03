import time
from typing import NoReturn

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from config import settings


class Instraper():
	def set_up_driver(self) -> webdriver:
		driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
		driver.get('https://www.instagram.com/')
		return driver

	def not_now_dismiss(self, driver: webdriver) -> WebDriverWait:
		return WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Не зараз")]'))
		).click()

	def scraping_data_by_hashtag(self, driver: webdriver, keyword: str) -> NoReturn:
		# Instagram Login:

		username_input_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="username"]')))
		password_input_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]')))
		username_input_field.clear()
		password_input_field.clear()
		username_input_field.send_keys(settings.instagram_username)
		password_input_field.send_keys(settings.instagram_password)
		
		log_in_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
		log_in_button.click()

		# Dismissing pop up messages:

		self.not_now_dismiss(driver)
		self.not_now_dismiss(driver)

		# Searching for a keyword:

		search_input_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Пошук"]')))
		search_input_field.clear()
		search_input_field.send_keys(keyword)
		time.sleep(5)
		keyword_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/" + keyword[1:] + "/')]")))
		keyword_link.click()

		# Scrolling down:

		# number_of_scrolls = 2
		# for i in range(0, number_of_scrolls):
		# 	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		# 	time.sleep(5)


if __name__ == '__main__':
	keyword = '#z'
	new_scrapper = Instraper()
	driver = new_scrapper.set_up_driver()
	new_scrapper.scraping_data_by_hashtag(driver, keyword)
