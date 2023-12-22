from selenium.webdriver.common.by import By
from scrape_link_info import scrape_link_info

def scrape_search_result (driver, element_pattern) :
    # Ambil elemen-elemen hasil pencarian
  search_results = driver.find_elements(
      By.XPATH, '//article[not(contains(@class, "video_tag"))]')

  for result in search_results:
    link_info = scrape_link_info(result,element_pattern)
    if link_info:
      # Cetak informasi
      print(f"Link: {link_info['link']}")
      print(f"Jumlah kemunculan keyword: {link_info['keyword_count']}")
      print(f"Judul: {link_info['judul']}")
      print(f"Tanggal Publikasi: {link_info['tanggal_publikasi']}")
      print(f"Deskripsi: {link_info['deskripsi']}")
      print("")
