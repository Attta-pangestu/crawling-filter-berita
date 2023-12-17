from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pygsheets
from math import ceil



links_metadata = []
# Inisialisasi driver Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def scrape_all_links(driver):
  # Ambil URL dari hasil pencarian
  search_results = driver.find_elements(By.XPATH, '//li[@class="b_algo"]/h2/a')
  result_links = [result.get_attribute('href') for result in search_results]
  return result_links

def get_link_info(result):
    # Cek apakah elemen tanggal publikasi ada
    date_element_exists = result.find_elements(By.CLASS_NAME, 'news_dt')
    if date_element_exists:
        time.sleep(2)
        # Ambil link
        link_element = result.find_element(By.XPATH, './/h2/a')
        link = link_element.get_attribute('href')

        # Ambil judul
        title_element = result.find_element(By.XPATH, './/h2/a')
        title = title_element.text.strip()

        # Ambil tanggal publikasi
        date_element = result.find_element(By.CLASS_NAME, 'news_dt')
        date = date_element.text.strip()

        return {
            "link": link,
            "judul": title,
            "tanggal_publikasi": date
        }

    return None



def scrape_all_results_info(driver):
  # Ambil elemen-elemen hasil pencarian
  search_results = driver.find_elements(By.XPATH, '//li[@class="b_algo"]')

  for result in search_results:
    link_info = get_link_info(result)
    if link_info:
        # Cetak informasi
        print(f"Link Berita: {link_info['link']}")
        print(f"Judul: {link_info['judul']}")
        print(f"Tanggal Publikasi: {link_info['tanggal_publikasi']}")
        print("")
        # Simpan informasi ke dalam struktur data yang sesuai
        links_metadata.append(link_info)


def set_filter_date_range(driver) :
    time.sleep(4)
    tools_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'scope_tools_wrapper')))
    tools_element.click()
    time.sleep(3)
    # Cari dan klik elemen "Date"
    date_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'b_tween_searchTools')))
    date_element.click()
    print('Memasukkan tanggal')
    # Masukkan tanggal mulai
    start_date_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'date_range_start')))
    start_date_input.clear()
    start_date_input.send_keys('01/01/2018')

    # Masukkan tanggal akhir
    end_date_input = driver.find_element(By.ID, 'date_range_end')
    end_date_input.clear()
    end_date_input.send_keys('01/01/2019')

    # Klik tombol "Apply"
    apply_button = driver.find_element(By.ID, 'time_filter_done_link')
    time.sleep(3)
    apply_button.send_keys(Keys.ENTER)
    print('Berhasil mengatur filter date range')

def search_bing_with_pagination(search_keyword, num_pages=10):
  # URL Bing
  bing_url = 'https://www.bing.com/'
  try:
    print('Membuka halaman Bing')
    # Buka Bing
    driver.get(bing_url)
    time.sleep(4)
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q")))
    time.sleep(1)
    # Masukkan kata kunci
    search_box.send_keys(search_keyword)
    time.sleep(1)
    # Tekan tombol Enter
    search_box.send_keys(Keys.ENTER)
    # Tunggu hingga halaman pencarian dimuat
    time.sleep(3)
    print('Memuat halaman hasil pencarian')
    for _page in range(num_pages):
      # Tunggu hingga hasil pencarian dimuat
      WebDriverWait(driver, 20).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, 'li.b_algo h2 a')))

      # Panggil fungsi untuk scrape semua link
      scrape_all_results_info(driver)

      # Cetak link untuk setiap halaman
      print(f'Didapatkan sebanyak {len(links_metadata)} tautan')

      # Coba temukan elemen untuk halaman berikutnya dan klik
      try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.sb_pagN')))
        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        next_button.click()

      except Exception as e:
        print(f"Tidak dapat menemukan elemen halaman berikutnya: {e}")
        break  # Keluar dari loop jika tidak dapat menemukan elemen halaman berikutnya

  finally:
    # Tutup browser setelah selesai
    driver.quit()


def gsheet_upload(array_link):
  try:
    # Buat objek klien
    client = pygsheets.authorize(
        service_account_file="kajian-ufuk-indonesia-b1e63d302e2e.json")

    # Buka spreadsheet berdasarkan nama/judulnya
    spreadsht = client.open("KUI_analysis_Scraping")

    # Buka worksheet berdasarkan nama/judulnya
    worksht = spreadsht.worksheet("title", "Sheet1")

    # Tambahkan data ke worksheet
    worksht.cell("A1").set_text_format("bold", True).value = "Item"

    # Jika mengupdate nilai untuk beberapa kolom, data
    # harus berada dalam format matriks
    link_matrix = [[link_info['link']] for link_info in array_link]
    worksht.update_values("A2", link_matrix)

    print("Tautan berhasil diunggah ke Google Sheets!")

  except Exception as e:
    print(f"Error mengunggah ke Google Sheets: {e}")


try:
  # Panggil fungsi pencarian dengan paginasi
  search_bing_with_pagination('kekeringan berita ', num_pages=2)
  # Update ke Google Sheets
  # gsheet_upload(links_metadata)

except Exception as main_error:
  # gsheet_upload(links_metadata)
  print(f"Program utama menemui kesalahan: {main_error}")
finally:
  # Tutup browser setelah selesai
  driver.quit()
