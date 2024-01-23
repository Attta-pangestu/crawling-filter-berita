# library
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Modul
from helper import init_driver
from scraping_utility import scrape_link_info


def search_with_pagination(keyword,search_link, element_pattern, domain,  num_pages=10):
    links_metadata = []

    try:
        driver = init_driver()
        driver.get(search_link)

        script_stop = "window.stop();"
        driver.execute_script(script_stop)
        links_metadata = scrape_search_result(keyword, driver, element_pattern, links_metadata, domain)

        for _page in range(1, num_pages + 1):
            print(f"Mencari next button pada halaman {_page}")
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, element_pattern['search_results']))
            )
            print(f'Didapatkan sebanyak {len(links_metadata)} tautan')

            # Cari indeks link saat ini
            current_index = (_page + 1) * 10  # Misalnya, 10 link per halaman

            # Coba temukan elemen untuk halaman berikutnya dan klik
            try:
                # Tambahkan parameter "first" ke URL
                next_link = f"{search_link}&first={current_index}"
                print(f"Navigasi ke: {next_link}")
                driver.get(next_link)
                print(f"Melakukan Scraping halaman {_page}")
                WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, element_pattern['search_results']))
                )
                links_metadata = scrape_search_result(keyword, driver, element_pattern, links_metadata, domain)


            except Exception as e:
                print(f"Tidak dapat menemukan elemen halaman berikutnya: {e}")
                break  # Keluar dari loop jika tidak dapat menemukan elemen halaman berikutnya

    except Exception as e:
        print(f"Error saat menjalankan *search_with_pagination* ", e)
    finally:
        # Tutup browser setelah selesai
        driver.quit()

    return links_metadata


def scrape_search_result (keyword, driver, element_pattern, links_metadata, domain) :
    print('Menjalankan scraping hasil pencarian', element_pattern['search_results'])
    # Ambil elemen-elemen hasil pencarian
    search_results = driver.find_elements(
        By.CSS_SELECTOR, element_pattern['search_results']);
    # Iterasi melalui setiap elemen hasil pencarian
    # for idx, result in enumerate(search_results, start=1):
    #     # Dapatkan HTML dari elemen
    #     element_html = driver.execute_script("return arguments[0].outerHTML;", result)   
    #     # Cetak HTML elemen
    #     print(f"HTML Elemen ke-{idx}:\n{element_html}\n")  
    
    for result in search_results:
        link_info = scrape_link_info(keyword,result,element_pattern, domain)
        
        if link_info:
            # Cetak informasi
            print(f"Link: {link_info['link']}")
            print(f"Jumlah kemunculan keyword: {link_info['keyword_count']}")
            print(f"Judul: {link_info['judul']}")
            print(f"Tanggal Publikasi: {link_info['tanggal_publikasi']}")
            print(f"Deskripsi: {link_info['deskripsi']}")
            print("")
            # Simpan informasi ke dalam struktur data yang sesuai
            links_metadata.append([
                link_info['link'],
                link_info['keyword'],
                link_info['judul'],
                link_info['deskripsi'],
                link_info['tanggal_publikasi'],
                link_info['keyword_count'],
            ])
    return links_metadata


