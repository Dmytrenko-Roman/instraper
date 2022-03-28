from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Instagram Login:

driver.get('https://www.instagram.com/')

time.sleep(5)
driver.close()
driver.quit()
