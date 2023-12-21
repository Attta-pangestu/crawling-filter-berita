import time
import pygsheets
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from gsheet_helper import gsheet_upload
import re
from datetime import datetime, timedelta
from date_convert_format import convert_date_format
from html_analisis.keyword_counter_filter import keyword_counter_filter

options = Options()
options.page_load_strategy = 'eager'
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

links_metadata = []
date_start = "01/01/2018"
date_end = "01/01/2023"
keyword = "kemarau"

links_metadata = []


def get_link_info(result):
  # Cek apakah elemen tanggal publikasi ada
  description_elements = result.find_elements(
      By.XPATH, './/p[@class="b_lineclamp4 b_algoSlug"]')
  date_elements = result.find_elements(By.CLASS_NAME, 'date')

  try:
    if date_elements:
      # Ambil Link
      link_element = result.find_element(By.XPATH, './/a')
      link_href = link_element.get_attribute('href')
      # Hitung jumlah keywordnya
      keyword_count = keyword_counter_filter(link_href, keyword)
      if keyword_count > 1:
        # Ambil judul
        title = result.find_element(By.CLASS_NAME, 'title').text.strip()

        # Ambil deskripsi
        description = result.find_element(By.XPATH, './/p').text.strip()

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


def scrape_all_results_info(driver):
  # Ambil elemen-elemen hasil pencarian
  search_results = driver.find_elements(
      By.XPATH, '//article[not(contains(@class, "video_tag"))]')

  for result in search_results:
    link_info = get_link_info(result)
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


def search_with_pagination(search_keyword, start_date, end_date, num_pages=10):
  global links_metadata
  try:
    detik_link = f"https://www.detik.com/search/searchall?query={search_keyword}&sortby=time&fromdatex={start_date}&todatex={end_date}&siteid=3"
    driver.get(detik_link)
    print(detik_link)

    # Menjalankan skrip JavaScript setelah halaman selesai dimuat
    # Sisipkan skrip JavaScript untuk menghentikan loading
    script_stop = "window.stop();"
    driver.execute_script(script_stop)
    scrape_all_results_info(driver)

    for _page in range(num_pages):
      # Tunggu hingga hasil pencarian dimuat
      print(f"Sedang mencari next button halaman {_page}")
      WebDriverWait(driver, 20).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, 'article')))
      # Panggil fungsi untuk scrape semua link
      scrape_all_results_info(driver)
      # Cetak link untuk setiap halaman
      print(f'Didapatkan sebanyak {len(links_metadata)} tautan')

      # Coba temukan elemen untuk halaman berikutnya dan klik
      try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '.paging a.last img[alt="Kanan"]')))

        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        next_button.click()

      except Exception as e:
        print(f"Tidak dapat menemukan elemen halaman berikutnya: {e}")
        break  # Keluar dari loop jika tidak dapat menemukan elemen halaman berikutnya

  finally:
    # Tutup browser setelah selesai
    driver.quit()


try:
  # Panggil fungsi pencarian dengan paginasi
  search_with_pagination(keyword, date_start, date_end, num_pages=200)
  # Update ke Google Sheets
  gsheet_upload(array_link=links_metadata, Sheet='Detik', update=True)

except Exception as main_error:
  gsheet_upload(array_link=links_metadata, Sheet='Detik', update=True)
  print(f"Program utama menemui kesalahan: {main_error}")
finally:
  # Tutup browser setelah selesai
  driver.quit()
