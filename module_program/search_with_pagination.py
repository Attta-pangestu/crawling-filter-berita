# library
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Modul
from driver.driver_helper import init_driver
from scraping_helper.scrape_search_result import scrape_search_result

def search_with_pagination(keyword,search_link, element_pattern, num_pages=10):
    links_metadata = []
    try:
        driver = init_driver()
        driver.get(search_link)

        script_stop = "window.stop();"
        driver.execute_script(script_stop)

        for _page in range(num_pages):
            print(f"Mencari next button pada halaman {_page + 1}")
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, element_pattern['search_results']))
            )
            links_metadata = scrape_search_result(keyword, driver, element_pattern, links_metadata)
            print(f'Didapatkan sebanyak {len(links_metadata)} tautan')

            # Coba temukan elemen untuk halaman berikutnya dan klik
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, element_pattern['next_elements']))
                )
                next_button.click()
            except Exception as e:
                print(f"Tidak dapat menemukan elemen halaman berikutnya: {e}")
                break  # Keluar dari loop jika tidak dapat menemukan elemen halaman berikutnya

    except Exception as e:
        print(f"Error saat menjalankan *search_with_pagination* ", e)
    finally:
        # Tutup browser setelah selesai
        driver.quit()

    return links_metadata


