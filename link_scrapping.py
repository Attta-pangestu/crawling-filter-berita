from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

from bs4 import BeautifulSoup


links = []

def scrape_all_links(driver):
    # Ambil URL dari hasil pencarian
    search_results = driver.find_elements("css selector", 'li.b_algo h2 a')
    result_links = [result.get_attribute('href') for result in search_results]
    
    # Menambahkan semua tautan ke dalam array links
    links.extend(result_links)
    
def search_bing_with_pagination(search_keyword, num_pages=10):
    # URL Bing
    bing_url = 'https://www.bing.com/'

    # Inisialisasi driver Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Buka Bing
        driver.get(bing_url)
        time.sleep(4)
        # Temukan elemen input pencarian
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )

        # Masukkan kata kunci
        search_box.send_keys(search_keyword)

        # Tekan tombol Enter
        search_box.send_keys(Keys.ENTER)

        time.sleep(3)


        # Ubah Filter Date Range
        # Cari dan klik elemen "Tools"
        tools_element = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.ID, 'scope_tools_wrapper'))) 
        tools_element.click()

        # Cari dan klik elemen "Date"
        date_element = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.ID, 'b_tween_searchTools'))) 
        date_element.click()

        # Masukkan tanggal mulai
        start_date_input = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.ID, 'date_range_start')))
        start_date_input.clear()
        start_date_input.send_keys('01/01/2018')

        # Masukkan tanggal akhir
        end_date_input = driver.find_element(By.ID, 'date_range_end')
        end_date_input.clear()
        end_date_input.send_keys('01/01/2020')

        # Klik tombol "Apply"
        apply_button = driver.find_element(By.ID, 'time_filter_done_link')
        apply_button.click()

        for page in range(num_pages):
            # Tunggu hingga hasil pencarian dimuat
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'li.b_algo h2 a'))
            )

            # Panggil fungsi untuk scrape semua link
            scrape_all_links(driver)

            # Cetak link untuk setiap halaman
            print(f"Hasil Pencarian untuk halaman {page + 1}:")
            for i, link in enumerate(links, start=1):
                print(f"{i}. {link}")

            # Coba temukan elemen untuk halaman berikutnya dan klik
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.sb_pagN'))
                )
                next_button.click()
            except Exception as e:
                print(f"Tidak dapat menemukan elemen halaman berikutnya: {e}")
                break  # Keluar dari loop jika tidak dapat menemukan elemen halaman berikutnya


    finally:
        # Tutup browser setelah selesai
        driver.quit()

# Panggil fungsi pencarian dengan paginasi
search_bing_with_pagination('pemilu', num_pages=30)
