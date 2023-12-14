from pygsheets.worksheet import Worksheet
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pygsheets
from pygsheets.exceptions import WorksheetNotFound
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

links = []


def scrape_all_links(driver):
  # Ambil URL dari hasil pencarian
  search_results = driver.find_elements(By.XPATH, '//li[@class="b_algo"]/h2/a')
  result_links = [result.get_attribute('href') for result in search_results]

  # Menambahkan semua tautan ke dalam array links
  links.extend(result_links)


def search_bing_with_pagination(search_keyword, num_pages=10):
  # URL Bing
  bing_url = 'https://www.bing.com/'

  # Inisialisasi driver Chrome
  try:
    # Buka Bing
    driver.get(bing_url)
    time.sleep(4)
    # Temukan elemen input pencarian
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q")))

    # Masukkan kata kunci
    search_box.send_keys(search_keyword)
    time.sleep(2)

    # Tekan tombol Enter
    search_box.send_keys(Keys.ENTER)

    for page in range(num_pages):
      # Tunggu hingga hasil pencarian dimuat
      WebDriverWait(driver, 20).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, 'li.b_algo h2 a')))

      # Panggil fungsi untuk scrape semua link
      scrape_all_links(driver)

      time.sleep(1)
      print(f'Didapatkan sebanyak {len(links)} tautan')
      # # Cetak link untuk setiap halaman
      # print(f"Hasil Pencarian untuk halaman {page + 1}:")
      # for i, link in enumerate(links, start=1):
      #   print(f"{i}. {link}")
      # Coba temukan elemen untuk halaman berikutnya dan klik
      try:
        time.sleep(2)
        next_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.sb_pagN')))
        driver.execute_script("arguments[0].click();", next_button)
      except Exception as e:
        print(f"Tidak dapat menemukan elemen halaman berikutnya: {e}")
        break  # Keluar dari loop jika tidak dapat menemukan elemen halaman berikutnya

  finally:
    # Tutup browser setelah selesai
    driver.quit()


def gsheet_upload(array_link):
  try:
    # Create the Client
    client = pygsheets.authorize(
        service_account_file="kajian-ufuk-indonesia-b1e63d302e2e.json")

    # opens a spreadsheet by its name/title
    spreadsht = client.open("KUI_analysis_Scraping")

    # opens a worksheet by its name/title
    worksht = spreadsht.worksheet("title", "Sheet1")

    # Now, let's add data to our worksheet

    # Creating the first column
    worksht.cell("A1").set_text_format("bold", True).value = "Item"

    # if updating multiple values, the data
    # should be in a matrix format
    link_matrix = [[link] for link in array_link]
    worksht.update_values("A2", link_matrix)  # Adding row values

    print("Links uploaded to Google Sheets successfully!")

  except Exception as e:
    print(f"Error uploading to Google Sheets: {e}")


try:
  # Panggil fungsi pencarian dengan paginasi
  search_bing_with_pagination('kekeringan berita tahun 2018 sampai 2023',
                              num_pages=400)
  # Update to Google Sheets
  gsheet_upload(links)

except Exception as main_error:
  gsheet_upload(links)
  print(f"Main program encountered an error: {main_error}")
finally:
  # Tutup browser setelah selesai
  driver.quit()
