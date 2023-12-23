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


from datetime import datetime

def ambil_tiga_kata_pertama(input_tanggal):
    kata_kata = input_tanggal.split()
    tiga_kata_pertama = kata_kata[:3]

    # Jika tiga kata pertama adalah angka (tanggal), tambahkan kata bulan yang sesuai
    if tiga_kata_pertama[0].isdigit():
        tiga_kata_pertama[1] = tiga_kata_pertama[1][:3]  # Ambil tiga karakter pertama dari nama bulan

    return ' '.join(tiga_kata_pertama)


def convert_date_format(input_date):
    input_date = ambil_tiga_kata_pertama(input_date)
    # Buat kamus untuk mapping nama bulan dalam bahasa Indonesia ke bahasa Inggris
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

    # Ubah nama bulan dalam input_date menjadi bahasa Inggris
    for id, en in bulan_mapping.items():  # Perhatikan urutan en, id dibalik
        input_date = input_date.replace(id, en)

    try:
        # Cek apakah input_date memiliki format jam (HH:MM)
        datetime.strptime(input_date, "%d %b %Y %H:%M")
        format_tanggal = "%d %b %Y %H:%M"
    except ValueError:
        # Jika tidak memiliki format jam, gunakan format tanggal saja
        format_tanggal = "%d %b %Y"

    # Coba parsing tanggal dan waktu
    date_object = datetime.strptime(input_date, format_tanggal)
    output_date = date_object.strftime("%m/%d/%Y")

    return output_date


import requests
from bs4 import BeautifulSoup

def keyword_counter_filter(link, keyword):
    try:
        # Mengambil konten HTML dari link
        response = requests.get(link)
        response.raise_for_status()  # Menangani HTTP error jika ada
        html_content = response.text

        # Parsing konten HTML menggunakan BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Menghitung jumlah kemunculan keyword dalam konten HTML
        keyword_count = soup.text.lower().count(keyword.lower())

        return keyword_count

    except Exception as e:
        print(f"Error dalam mengambil atau menghitung keyword di link {link}: {e}")
        return 0

