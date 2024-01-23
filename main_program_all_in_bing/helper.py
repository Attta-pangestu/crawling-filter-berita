from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse



# Fungsi untuk menginisialisasi driver
def init_driver():
    chrome_options = Options()
    chrome_options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


def is_valid_domain(link, main_domain):
    parsed_url = urlparse(link)
    # Dapatkan domain dari link
    link_domain = parsed_url.netloc
    
    # Pisahkan domain menjadi bagian subdomain dan domain utama
    subdomains = link_domain.split('.')
    
    # Jika domain utama sama dengan yang diinginkan
    if subdomains[-2:] == main_domain.split('.')[-2:]:
        return True
    
    return False

def convert_date_filter_bing(date_string):
  reference_date = datetime(1970, 1, 11)
  target_date = datetime.strptime(date_string, '%d/%m/%Y')
  days_difference = (target_date - reference_date).days
  return days_difference


from datetime import datetime, timedelta


# Fungsi untuk mengambil tiga kata pertama dari tanggal
def ambil_tiga_kata_pertama(input_tanggal):
    kata_kata = input_tanggal.split()
    tiga_kata_pertama = kata_kata[:3]

    if tiga_kata_pertama[0].isdigit():
        tiga_kata_pertama[1] = tiga_kata_pertama[1][:3]

    return ' '.join(tiga_kata_pertama)

bulan_mapping = {
    'Jan': 'Jan',
    'Feb': 'Feb',
    'Mar': 'Mar',
    'Apr': 'Apr',
    'Mei': 'May',  # Ganti 'Mei' ke 'May'
    'Jun': 'Jun',
    'Jul': 'Jul',
    'Agu': 'Aug',  # Ganti 'Agu' ke 'Aug'
    'Sep': 'Sep',
    'Okt': 'Oct',
    'Nov': 'Nov',
    'Des': 'Dec'
}

# Fungsi untuk mengonversi format tanggal
def convert_date_format(input_date):
    try:
        format_tanggal = "%b %d, %Y %H:%M" if ':' in input_date else "%b %d, %Y"

        for id, en in bulan_mapping.items():
            input_date = input_date.replace(id, en)

        date_object = datetime.strptime(input_date, format_tanggal)
        output_date = date_object.strftime("%m/%d/%Y")  # Mengganti format keluaran ke "MM/DD/YYYY"

        return output_date

    except ValueError as ve:
        print(f"Error dalam mengonversi format tanggal: {ve}")
        return None


# Fungsi untuk menghitung kemunculan keyword
def keyword_counter_filter(link, keyword):
    try:
        response = requests.get(link)
        response.raise_for_status()
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        keyword_count = soup.text.lower().count(keyword.lower())
        return keyword_count

    except Exception as e:
        print(f"Error dalam mengambil atau menghitung keyword di link {link}: {e}")
        return 0
