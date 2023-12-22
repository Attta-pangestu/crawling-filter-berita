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

