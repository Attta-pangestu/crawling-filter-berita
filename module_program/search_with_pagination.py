# library
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Modul
from driver.driver_helper import init_driver
from scraping_helper.scrape_search_result import scrape_search_result

def search_with_pagination(search_link, element_pattern, num_pages=10):
    links_metadata = []
    try : 
        driver = init_driver()
        driver.get(search_link)

        script_stop = "window.stop();"
        driver.execute_script(script_stop)
        scrape_result = scrape_search_result(driver, element_pattern)
        links_metadata.append(scrape_result)
        
        for _page in range(num_pages) :
            print(f"Mencari next button pada halaman {num_pages + 1}")
            WebDriverWait(driver,10).until(

            )

    except Exception as e: 
        print(f"Error saat menjalankan *search_with_pagination* ", {e})
