from selenium.webdriver.common.by import By
from keyword_helper.keyword_counter_html import keyword_counter_filter
from date_helper.date_convert_format import convert_date_format

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