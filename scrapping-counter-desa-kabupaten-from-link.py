import requests
from bs4 import BeautifulSoup
import re

def crawl_and_analyze(url):
    # Mendapatkan HTML dari halaman berita
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
    else:
        print(f"Gagal mendapatkan halaman {url}. Status code: {response.status_code}")
        return None

    # Menggunakan BeautifulSoup untuk parsing HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Mencari semua paragraf di dalam konten berita
    paragraphs = soup.find_all('p')

    # Mencari nama desa dari teks paragraf
    desa_mentions = set()
    for paragraph in paragraphs:
        text = paragraph.get_text().lower()

        # Mencari kata 'desa' di awal teks paragraf
        desa_match = re.search(r'\bdesa (\w+)', text)
        if desa_match:
            desa_name = desa_match.group(1)
            desa_mentions.add(desa_name)

    # Mencari nama desa dari alt teks gambar
    images = soup.find_all('img')
    for image in images:
        alt_text = image.get('alt', '').lower()
        desa_match = re.search(r'\bdesa (\w+)', alt_text)
        if desa_match:
            desa_name = desa_match.group(1)
            desa_mentions.add(desa_name)

    return desa_mentions

def main():
    # List hasil pencarian dan linknya
    search_results = [
        {'title': 'NTB dan NTT Hadapi Bencana Kekeringan', 'link': 'https://www.voaindonesia.com/a/ntb-dan-ntt-hadapi-bencana-kekeringan/6212316.html'},
        {'title': 'Korban Kekeringan (Jiwa), 2020-2022 - BPS Provinsi NTT', 'link': 'https://ntt.bps.go.id/indicator/27/913/1/korban-kekeringan.html'},
        {'title': 'Berita Harian Kekeringan Di Ntt Terbaru Hari Ini', 'link': 'https://www.kompas.com/tag/kekeringan+di+ntt'},
        {'title': 'Ancaman Kekeringan Melanda NTT. Apa yang Harus Dilakukan?', 'link': 'https://www.mongabay.co.id/2021/07/25/ancaman-kekeringan-melanda-ntt-apa-yang-harus-dilakukan/'}
        # Tambahkan hasil pencarian lainnya sesuai kebutuhan
    ]

    for result in search_results:
        print(f"\nAnalisis Desa pada Berita: {result['title']}")
        desa_mentions = crawl_and_analyze(result['link'])

        if desa_mentions:
            print("Desa yang disebut:")
            for desa in desa_mentions:
                print(f"- {desa}")

if __name__ == "__main__":
    main()
