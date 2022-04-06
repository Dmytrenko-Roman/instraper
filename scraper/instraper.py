import time
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from config import settings
from database import post_collection


class Instraper:
    cities_filename = "cities.txt"

    def set_up_driver(self, url: str) -> webdriver:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(url)
        return driver

    def not_now_dismiss(self, driver: webdriver) -> WebDriverWait:
        return (
            WebDriverWait(driver, 10)
            .until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[contains(text(), "Не зараз")]')
                )
            )
            .click()
        )

    def check_owner_location(self, owner_location: str) -> bool:
        with open(self.cities_filename, "r") as fr:
            cities = json.load(fr)

        result = False
        for city in cities:
            if city in owner_location:
                result = True

        return result

    def scraping_cities_by_country_name(self, driver: webdriver) -> None:
        cities_list = []

        while True:
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//div[contains(@class, 'vLP4P')]")
                    )
                )
                next_button.click()
            except:
                break
            time.sleep(3)

        cities = driver.find_elements(By.XPATH, "//a[contains(@class, 'aMwHK')]")

        for city in cities:
            cities_list.append(city.text)

        with open(self.cities_filename, "w") as fw:
            json.dump(cities_list, fw)

    def scraping_data_by_hashtag(
        self, driver: webdriver, keyword: str, limit: int
    ) -> None:
        # Instagram Login:

        username_input_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="username"]'))
        )
        password_input_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]'))
        )
        username_input_field.clear()
        password_input_field.clear()
        username_input_field.send_keys(settings.instagram_username)
        password_input_field.send_keys(settings.instagram_password)

        log_in_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
        )
        log_in_button.click()

        # Dismissing pop up messages:

        self.not_now_dismiss(driver)
        self.not_now_dismiss(driver)

        # Searching for a keyword:

        search_input_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Пошук"]'))
        )
        search_input_field.clear()
        search_input_field.send_keys(keyword)

        time.sleep(5)

        keyword_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, '-qQT3')]"))
        )
        keyword_link.click()

        # Trying to get data of each post:

        time.sleep(5)

        all_posts = driver.find_elements(By.TAG_NAME, "a")
        all_posts_links = []
        post_counter = 0
        for post in all_posts:
            post_link = post.get_attribute("href")
            if "/p/" in post_link:
                all_posts_links.append(post_link.split(".com", 1)[1])

            # Limiting the posts:

            post_counter += 1
            if post_counter == limit:
                break

        for link in all_posts_links:
            time.sleep(5)

            post_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//a[contains(@href, '{link}')]")
                )
            )
            post_link.click()

            time.sleep(5)

            post_owner = driver.find_element(
                By.XPATH, "//a[contains(@class, 'sqdOP yWX7d     _8A5w5   ZIAjV ')]"
            ).text

            try:
                post_owner_location = driver.find_element(
                    By.XPATH, "//a[contains(@class, 'O4GlU')]"
                ).text
            except:
                post_owner_location = None

            post_owner_url = driver.find_element(
                By.XPATH, "//a[contains(@class, 'sqdOP yWX7d     _8A5w5   ZIAjV ')]"
            ).get_attribute("href")
            post_description = driver.find_element(
                By.XPATH,
                "//span[contains(@class, '_7UhW9   xLCgt      MMzan   KV-D4           se6yk       T0kll ')]",
            ).text
            post_image_url = driver.find_element(
                By.XPATH, "//img[contains(@class, 'FFVAD')]"
            ).get_attribute("src")

            if self.check_owner_location():

                post_collection.create_post(
                    post_owner,
                    post_owner_location,
                    post_owner_url,
                    post_description,
                    post_image_url,
                )

            time.sleep(5)

            close_the_post = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class, 'wpO6b  ')]")
                )
            )
            close_the_post.click()
