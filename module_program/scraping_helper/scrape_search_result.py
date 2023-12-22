from selenium.webdriver.common.by import By
from scraping_helper.scrape_link_info import scrape_link_info

def scrape_search_result (keyword, driver, element_pattern, links_metadata) :
    # Ambil elemen-elemen hasil pencarian
  search_results = driver.find_elements(
      By.XPATH, element_pattern['search_results'])

  for result in search_results:
    link_info = scrape_link_info(keyword,result,element_pattern)
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
