from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

# Melakukan pencarian Google dengan kata kunci "kkeringan"
search_keyword = "kkeringan"

# Mengakses halaman pertama hasil pencarian
google_search_url = f"https://www.google.com/search?q={search_keyword}"
driver.get(google_search_url)

# Mencatat link hasil pencarian pada 5 halaman pertama
for page in range(10):
    print(f"\nHasil Pencarian untuk kata kunci: {search_keyword}, Halaman: {page + 1}\n")
    c = 1

    # Mencatat link pada halaman saat ini
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    search_results = soup.find_all('div', class_='tF2Cxc')
    for result in search_results:
        link_element = result.find('a')
        link = link_element.get('href')
        print(str(c) + ". " + link)
        c += 1

    # Mencari elemen "Hasil lainnya" dan mengkliknya
    try:
        more_results_element = driver.find_element(By.XPATH, "//span[contains(text(), 'More results')]")
        more_results_element.click()
    except:
        print("Tidak dapat menemukan elemen 'Hasil lainnya'.")

    # Menjalankan infinite scroll
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Menunggu sejenak untuk memastikan konten baru telah dimuat
    time.sleep(2)

# Quitting the browser
driver.quit()
