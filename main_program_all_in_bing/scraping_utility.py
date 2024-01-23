from selenium.webdriver.common.by import By


from helper import keyword_counter_filter
from helper import convert_date_format
from helper import is_valid_domain

def  scrape_link_info(keyword, result, element_pattern, domain):
    try:
        date_elements = result.find_elements(By.CSS_SELECTOR, element_pattern['date_elements'])
        link_element = result.find_element(By.CSS_SELECTOR, element_pattern['link_elements'])
        link_href = link_element.get_attribute('href')
        if date_elements :
            print({domain, link_href})
            if( is_valid_domain(link= link_href, main_domain=domain)) :
                print("Termasuk domain utama")
            # Ambil Link
            # Hitung jumlah keywordnya
            # keyword_count = keyword_counter_filter(link_href, keyword)
            keyword_count = 10
            if keyword_count > 2:
                # Ambil judul
                title = link_element.text.strip()
                # Ambil deskripsi
                description = result.find_element(By.CSS_SELECTOR, element_pattern['description_elements']).text.strip()
                description = description.split(" · ", 1)[1]
                # Ambil tanggal publikasi
                raw_date = date_elements[0].text.strip()
                
                date = convert_date_format(raw_date)

                return {
                    "link": link_href,
                    "keyword": keyword,
                    "judul": title,
                    "deskripsi": description,
                    "tanggal_publikasi": date,
                    "keyword_count": keyword_count
                }
        return None
    except Exception as e:
        print(f"Error dalam mengambil informasi link: {e}")
        return None

    return None


