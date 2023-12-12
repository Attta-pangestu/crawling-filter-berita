from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

def scrape_all_links(driver, search_keyword):
    # Ambil URL dari hasil pencarian
    search_results = driver.find_elements("css selector", 'li.b_algo h2 a')
    result_links = [result.get_attribute('href') for result in search_results]

    # Tampilkan hasil
    print(f"Hasil Pencarian untuk '{search_keyword}':")
    for i, link in enumerate(result_links, start=1):
        print(f"{i}. {link}")

def search_bing_with_pagination(search_keyword, num_pages=10):
    # URL Bing
    bing_url = 'https://www.bing.com/'

    # Inisialisasi driver Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Buka Bing
        driver.get(bing_url)

        # Temukan elemen input pencarian
        search_box = driver.find_element("name", "q")

        # Masukkan kata kunci
        search_box.send_keys(search_keyword)

        # Tekan tombol Enter
        search_box.send_keys(Keys.ENTER)

        for page in range(num_pages):
            # Tunggu beberapa detik untuk melihat hasil pencarian
            time.sleep(5)

            # Panggil fungsi untuk scrape semua link
            scrape_all_links(driver, search_keyword)

            # Coba temukan elemen untuk halaman berikutnya dan klik
            try:
                next_button = driver.find_element("css selector", 'a.sb_pagN')
                next_button.click()
            except Exception as e:
                print(f"Tidak dapat menemukan elemen halaman berikutnya: {e}")
                break  # Keluar dari loop jika tidak dapat menemukan elemen halaman berikutnya

            # Tunggu sampai halaman baru dimuat
            time.sleep(5)

    finally:
        # Tutup browser setelah selesai
        driver.quit()

# Panggil fungsi pencarian dengan paginasi
search_bing_with_pagination('kekeringan', num_pages=10)
