from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
dr = webdriver.Chrome(options=options)

# Melakukan pencarian Google dengan kata kunci "kkeringan"
search_keyword = "kkeringan"
google_search_url = f"https://www.google.com/search?q={search_keyword}"
dr.get(google_search_url)

# Mencatat link hasil pencarian
print("Hasil Pencarian untuk kata kunci:", search_keyword)
c = 1
for i in dr.find_elements(By.CSS_SELECTOR, 'div.tF2Cxc'):
    link_element = i.find_element(By.CSS_SELECTOR, 'a')
    link = link_element.get_attribute('href')
    print(str(c) + ". " + link)
    c += 1

# Quitting the browser
dr.quit()
