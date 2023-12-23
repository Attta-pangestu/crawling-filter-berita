from selenium.webdriver.common.by import By


from helper import keyword_counter_filter
from helper import convert_date_format

def scrape_link_info(keyword, result, element_pattern):
    date_elements = result.find_elements(By.XPATH, element_pattern['date_elements'])
    try:
        if date_elements:
            # Ambil Link
            link_element = result.find_element(By.XPATH, element_pattern['link_elements'])
            link_href = link_element.get_attribute('href')
            # Hitung jumlah keywordnya
            keyword_count = keyword_counter_filter(link_href, keyword)
            if keyword_count > 1:
                # Ambil judul
                title = result.find_element(By.CLASS_NAME, element_pattern['title_elements']).text.strip()

                # Ambil deskripsi
                description = result.find_element(By.XPATH, element_pattern['description_elements']).text.strip()

                # Ambil tanggal publikasi
                raw_date = date_elements[0].text.strip()
                
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



from selenium.webdriver.common.by import By


def scrape_search_result (keyword, driver, element_pattern, links_metadata) :
    print('Menjalankan scraping hasil pencarian', element_pattern['search_results'])
    # Ambil elemen-elemen hasil pencarian
    search_results = driver.find_elements(
        By.XPATH, element_pattern['search_results'])
    print(search_results)
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


