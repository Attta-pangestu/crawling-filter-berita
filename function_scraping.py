import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
from selenium.common.exceptions import NoSuchElementException

# Fixed module
from helper import init_driver
from helper import keyword_counter_filter
from helper import convert_date_format
from helper import gsheet_upload

def scrape_link_info(keyword, result, elements_pattern):
  date_elements = result.find_elements(By.CSS_SELECTOR,
                                       elements_pattern['date_elements'])
  try:
    if date_elements:
      # Ambil Link
      link_element = result.find_element(By.XPATH,
                                         elements_pattern['link_elements'])
      link_href = link_element.get_attribute('href')

      # Hitung jumlah keywordnya
      keyword_count = keyword_counter_filter(link_href, keyword)

      if keyword_count > 1:

        # Ambil judul
        title = result.find_element(
            By.CLASS_NAME, elements_pattern['title_elements']).text.strip()

        # Ambil deskripsi
        description = result.find_element(
            By.XPATH, elements_pattern['description_elements']).text.strip()

        # Ambil tanggal publikasi
        raw_date = date_elements[0].text.strip()
        match = re.search(r'\w+, (\d+ \w+ \d+ \d+:\d+) WIB', raw_date)
        date = match.group(1) if match else "Format tanggal tidak sesuai"
        date = convert_date_format(date)

        return {
            "link": link_href,
            "keyword": keyword,
            "judul": title,
            "deskripsi": description,
            "tanggal_publikasi": date,
            "keyword_count": keyword_count
        }

  except Exception as e:
    print(f"Error dalam mengambil informasi link: {e}")
    return None

  return None


def scrape_search_result(keyword, driver, elements_pattern):
  links_scrape = []
  # Ambil elemen-elemen hasil pencarian
  search_results = driver.find_elements(By.XPATH,
                                        elements_pattern['search_elements'])
  for result in search_results:
    link_info = scrape_link_info(keyword, result, elements_pattern)
    if link_info:
      # Cetak informasi
      print("                        ****       ")
      print(f"Link: {link_info['link']}")
      print(f"Jumlah kemunculan keyword: {link_info['keyword_count']}")
      print(f"Judul: {link_info['judul']}")
      print(f"Tanggal Publikasi: {link_info['tanggal_publikasi']}")
      print(f"Deskripsi: {link_info['deskripsi']}")
      print("")
      print("                        ****       ")
      # Simpan informasi ke dalam struktur data yang sesuai
      links_scrape.append([
          link_info['link'],
          link_info['keyword'],
          link_info['judul'],
          link_info['deskripsi'],
          link_info['tanggal_publikasi'],
          link_info['keyword_count'],
      ])
  return links_scrape


def search_with_pagination(keyword,
                           search_link,
                           elements_pattern,
                           num_pages=10):
  driver = init_driver()
  links_whole_page = []
  links_scrape = []
  try:
    driver.get(search_link)
    print(f"Sedang mengakses link {search_link}\n")
    script_stop = "window.stop();"
    driver.execute_script(script_stop)

    for _page in range(num_pages):
      print("============================================")
      print(f"Melakukan Scraping Halaman {_page + 1}\n")
      print("============================================\n")

      WebDriverWait(driver, 20).until(
          EC.presence_of_element_located(
              (By.CSS_SELECTOR, elements_pattern['title_elements'])))

      links_scrape = scrape_search_result(keyword, driver, elements_pattern)

      links_whole_page.extend(links_scrape)

      print("============================================")
      print(f"Didapatkan sebanyak {len(links_whole_page)} tautan\n")
      print("============================================\n")

      # Coba temukan elemen untuk halaman berikutnya dan klik
      try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, elements_pattern['next_elements'])))
        next_button.click()
      except Exception as e:
        print(f"Tidak dapat menemukan elemen halaman berikutnya: {e}")
        break  # Keluar dari loop jika tidak dapat menemukan elemen halaman berikutnya

  except Exception as e:
    print(f"Error saat menjalankan *search_with_pagination* {e}")
  finally:
    # Tutup browser setelah selesai
    driver.quit()
  return links_whole_page


detik_pattern = {
    'search_elements': '//article[not(contains(@class, "video_tag"))]',
    'next_elements': '.paging a.last img[alt="Kanan"]',
    'description_elements': './/p',
    'date_elements': ".date",
    'link_elements': ".//a",
    'title_elements': "title",
}

try:
  dummy_link = "https://www.detik.com/search/searchall?query=kekeringan&sortby=time&fromdatex=01/01/2018&todatex=01/01/2023&siteid=3"
  all_result_scraping = search_with_pagination(keyword='kekeringan',
                                               search_link=dummy_link,
                                               elements_pattern=detik_pattern,
                                               num_pages=2)
  gsheet_upload('')
  print("============================================")
  print("MENGUPLOAD KE GOOGLE SHEET BERHASIL ")
  print("============================================\n")
  
except Exception as e:
  print(f"Terjadi error pada *scraping_link*: {e}")


