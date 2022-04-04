import time
from typing import NoReturn

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from config import settings
from database import post_collection


class Instraper():
	def set_up_driver(self) -> webdriver:
		driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
		driver.get(url='https://www.instagram.com/')
		return driver

	def not_now_dismiss(self, driver: webdriver) -> WebDriverWait:
		return WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Не зараз")]'))
		).click()

	def scraping_data_by_hashtag(self, driver: webdriver, keyword: str, limit: int) -> NoReturn:
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

		# Trying to get data of each post:

		time.sleep(5)
		all_posts = driver.find_elements(By.TAG_NAME, 'a')
		all_posts_links = []
		for post in all_posts:
			post_link = post.get_attribute('href')
			if '/p/' in post_link:
				all_posts_links.append(post_link.split('.com', 1)[1])

		post_counter = 0
		for link in all_posts_links:
			time.sleep(5)
			post_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//a[contains(@href, '{link}')]")))
			post_link.click()

			time.sleep(5)
			post_owner = driver.find_element(By.XPATH, "//a[contains(@class, 'sqdOP yWX7d     _8A5w5   ZIAjV ')]").text
			post_owner_url = driver.find_element(By.XPATH, "//a[contains(@class, 'sqdOP yWX7d     _8A5w5   ZIAjV ')]").get_attribute('href')
			post_description = driver.find_element(By.XPATH, "//span[contains(@class, '_7UhW9   xLCgt      MMzan   KV-D4           se6yk       T0kll ')]").text
			post_image_url = driver.find_element(By.XPATH, "//img[contains(@class, 'FFVAD')]").get_attribute('src')

			post_collection.create_post(post_owner, post_owner_url, post_description, post_image_url)

			time.sleep(5)
			close_the_post = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'wpO6b  ')]")))
			close_the_post.click()

			# Limiting the posts:

			post_counter += 1
			if post_counter == limit:
				break
