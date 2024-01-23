from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Function to initialize the driver
def init_driver():
    chrome_options = Options()
    chrome_options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


def is_valid_domain(url, domain):
    parsed_url = urlparse(url)
    # Dapatkan domain dari URL
    url_domain = parsed_url.netloc

    # Jika domain utama sama dengan yang diinginkan atau merupakan subdomain dari domain yang diinginkan
    if url_domain == domain or url_domain.endswith("." + domain):
        return True

    return False


def convert_date_filter_bing(date_string):
    reference_date = datetime(1970, 1, 11)
    target_date = datetime.strptime(date_string, '%d/%m/%Y')
    days_difference = (target_date - reference_date).days
    return days_difference

from datetime import datetime, timedelta

# Function to get the first three words from the date
def get_first_three_words(input_date):
    words = input_date.split()
    first_three_words = words[:3]

    if first_three_words[0].isdigit():
        first_three_words[1] = first_three_words[1][:3]

    return ' '.join(first_three_words)

month_mapping = {
    'Jan': 'Jan',
    'Feb': 'Feb',
    'Mar': 'Mar',
    'Apr': 'Apr',
    'Mei': 'May',
    'Jun': 'Jun',
    'Jul': 'Jul',
    'Agu': 'Aug',
    'Sep': 'Sep',
    'Okt': 'Oct',
    'Nov': 'Nov',
    'Des': 'Dec'
}

# Function to convert date format
def convert_date_format(input_date):
    try:
        date_format = "%b %d, %Y %H:%M" if ':' in input_date else "%b %d, %Y"

        for id, en in month_mapping.items():
            input_date = input_date.replace(id, en)

        date_object = datetime.strptime(input_date, date_format)
        output_date = date_object.strftime("%m/%d/%Y")

        return output_date

    except ValueError as ve:
        print(f"Error converting date format: {ve}")
        return None

# Function to count keyword occurrences
def keyword_counter_filter(link, keyword):
    try:
        response = requests.get(link)
        response.raise_for_status()
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        keyword_count = soup.text.lower().count(keyword.lower())
        return keyword_count

    except Exception as e:
        print(f"Error fetching or counting keyword in link {link}: {e}")
        return 0