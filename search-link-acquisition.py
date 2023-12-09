from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
dr = webdriver.Chrome(options=options)

# Membuka halaman pencarian Google
dr.get("https://www.google.com")

# Mengisi kotak pencarian dengan kata kunci "kkeringan"
search_box = dr.find_element(By.NAME, 'q')
search_box.send_keys("kekeringan")
search_box.send_keys(Keys.RETURN)

# Menemukan elemen "Alat" dan mengkliknya
tools_element = WebDriverWait(dr, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Alat')]"))
)
tools_element.click()

# Menunggu hingga elemen "Any time" muncul dan mengkliknya
any_time_element = WebDriverWait(dr, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Any time')]"))
)
any_time_element.click()

# Menunggu hingga elemen "Custom range..." muncul dan mengkliknya
custom_range_element = WebDriverWait(dr, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Custom range...')]"))
)
custom_range_element.click()

# Menunggu sejenak untuk elemen tanggal muncul
tanggal_awal_element = WebDriverWait(dr, 10).until(
    EC.visibility_of_element_located((By.ID, "OouJcb"))
)

# Menemukan elemen input untuk tanggal awal dan mengisinya
tanggal_awal_element.clear()
tanggal_awal_element.send_keys("01/01/2023")

# Menunggu sejenak untuk elemen tanggal akhir muncul
tanggal_akhir_element = WebDriverWait(dr, 10).until(
    EC.visibility_of_element_located((By.ID, "rzG2be"))
)

# Menemukan elemen input untuk tanggal akhir dan mengisinya
tanggal_akhir_element.clear()
tanggal_akhir_element.send_keys("12/31/2023")

# Menunggu hingga elemen tombol "Go" muncul dan mengkliknya
go_button = WebDriverWait(dr, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//g-button[contains(text(), 'Go')]"))
)
go_button.click()

# Menunggu sejenak untuk hasil filter waktu diaplikasikan
dr.implicitly_wait(3)

# Menampilkan hasil pencarian setelah filter waktu
hasil_pencarian = dr.find_elements(By.XPATH, "//div[@class='tF2Cxc']")
for i, item in enumerate(hasil_pencarian, start=1):
    title = item.find_element(By.XPATH, ".//h3").text
    link = item.find_element(By.XPATH, ".//a").get_attribute('href')
    print(f"{i}. Judul: {title}")
    print(f"   Link: {link}")
    print()

# Quitting the browser
dr.quit()
