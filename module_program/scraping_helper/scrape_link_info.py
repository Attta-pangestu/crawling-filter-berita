from selenium.webdriver.common.by import By

def scrape_link_info(result, element_pattern):
    date_elements = result.find_elements(By.XPATH, element_pattern[''])