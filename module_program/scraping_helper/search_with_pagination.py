from driver.driver_helper import init_driver


def search_with_pagination(search_link, num_pages=10):
    links_metadata = []
    try : 
        driver = init_driver()

    except Exception as e: 
        print(f"Error saat menjalankan *search_with_pagination* ", {e})