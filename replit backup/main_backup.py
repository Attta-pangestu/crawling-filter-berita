import time

from helper import init_driver

# library
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Modul
from helper import init_driver
from scraping_utility import scrape_link_info


def search_with_pagination(keyword,
                           search_link,
                           element_pattern,
                           num_pages=10):
  links_metadata = []

  try:
    driver = init_driver()
    driver.get(search_link)

    script_stop = "window.stop();"
    driver.execute_script(script_stop)
    links_metadata = scrape_search_result(keyword, driver, element_pattern,
                                          links_metadata)
    for _page in range(num_pages):
      print(f"Mencari next button pada halaman {_page + 1}")
      WebDriverWait(driver, 10).until(
          EC.presence_of_all_elements_located(
              (By.CSS_SELECTOR, element_pattern['search_results'])))
      links_metadata = scrape_search_result(keyword, driver, element_pattern,
                                            links_metadata)
      print(f'Didapatkan sebanyak {len(links_metadata)} tautan')

      # Coba temukan elemen untuk halaman berikutnya dan klik
      try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, element_pattern['next_elements'])))
        next_button.click()
      except Exception as e:
        print(f"Tidak dapat menemukan elemen halaman berikutnya: {e}")
        break  # Keluar dari loop jika tidak dapat menemukan elemen halaman berikutnya

  except Exception as e:
    print(f"Error saat menjalankan *search_with_pagination* {e}")
  finally:
    # Tutup browser setelah selesai
    driver.quit()

  return links_metadata


def scrape_search_result(keyword, driver, element_pattern, links_metadata):
  print('Menjalankan scraping hasil pencarian',
        element_pattern['search_results'])
  # Ambil elemen-elemen hasil pencarian
  search_results = driver.find_elements(By.XPATH,
                                        element_pattern['search_results'])
  print(search_results)
  for result in search_results:
    link_info = scrape_link_info(keyword, result, element_pattern)
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


# Inisiasi variabel
from link_interface import generate_array_search

try:
  # Dapatkan array pencarian dari antarmuka
  interprete_interface = generate_array_search()
  array_search = interprete_interface[0]
  keyword = interprete_interface[1]

  # Iterasi melalui setiap elemen dalam array pencarian
  for source, data in array_search.items():
    link = data['link']
    element_pattern = data['pattern']

    # Panggil fungsi pencarian dengan paginasi
    links_metadata = search_with_pagination(keyword,
                                            link,
                                            element_pattern,
                                            num_pages=2)

except Exception as e:
  print(f"Terjadi error pada *scraping_link*: {e}")
