from instraper import Instraper

if __name__ == "__main__":
    keyword = "#занаших"
    limit_of_posts = 3
    new_scrapper = Instraper()
    driver = new_scrapper.set_up_driver("https://www.instagram.com/")
    new_scrapper.scraping_data_by_hashtag(driver, keyword, limit_of_posts)

    # It's one time thing:
    # driver_for_scraping_cities = new_scrapper.set_up_driver("https://www.instagram.com/explore/locations/UA/ukraine/")
    # new_scrapper.scraping_cities_by_country_name(driver_for_scraping_cities)
