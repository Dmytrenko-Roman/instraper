from instraper import Instraper

if __name__ == "__main__":
    keyword = "#z"
    limit_of_posts = 1
    new_scrapper = Instraper()
    driver = new_scrapper.set_up_driver()
    new_scrapper.scraping_data_by_hashtag(driver, keyword, limit_of_posts)
