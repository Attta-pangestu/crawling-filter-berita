
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def init_driver():
    # Membuat objek ChromeOptions
    chrome_options = Options()
    # Mengatur strategi pemuatan halaman menjadi eager
    chrome_options.page_load_strategy = 'eager'

    # Membuat driver dengan opsi yang telah diatur
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    return driver