from instraper import Instraper

if __name__ == "__main__":
    new_scrapper = Instraper()
    keyword = "#занаших"
    limit_of_scrolls = 1
    driver = new_scrapper.set_up_driver("https://www.instagram.com/")
    new_scrapper.scraping_data_by_hashtag(driver, keyword, limit_of_scrolls)

    # It's one time thing:
    # driver_for_scraping_cities = new_scrapper.set_up_driver("https://www.instagram.com/explore/locations/UA/ukraine/")
    # new_scrapper.scraping_cities_by_country_name(driver_for_scraping_cities)
