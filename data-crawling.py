# Install library yang diperlukan
!pip install feedparser

import feedparser
from datetime import datetime

def crawl_berita(lokasi, kata_kunci, tahun, jumlah_berita):
    tanggal_awal = f'{tahun}-01-01T00:00:00Z'
    tanggal_akhir = f'{tahun+1}-01-01T00:00:00Z'


    url = f'https://news.google.com/rss/search?q={kata_kunci}+location:{lokasi}&hl=id&gl=ID&ceid=ID:en&time={tanggal_awal}_{tanggal_akhir}'


    feed = feedparser.parse(url)

    berita_dict = {'judul': [], 'link': [], 'deskripsi': []}

    for entry in feed.entries[:jumlah_berita]:
        judul = entry.title
        link = entry.link
        deskripsi = entry.summary
        berita_dict['judul'].append(judul)
        berita_dict['link'].append(link)
        berita_dict['deskripsi'].append(deskripsi)


    simpulan = analyze_berita(berita_dict['judul'], kata_kunci)

    return berita_dict, simpulan

def analyze_berita(judul_berita, kata_kunci):

    total_berita = len(judul_berita)
    berita_kunci = [judul for judul in judul_berita if kata_kunci.lower() in judul.lower()]
    total_berita_kunci = len(berita_kunci)

    return f'Dari total {total_berita} berita, {total_berita_kunci} berita mengandung kata kunci.'




# Contoh pemanggilan fungsi dengan lokasi 'Jakarta', kata kunci 'kekeringan', tahun '2020', dan jumlah berita '10'
tahun_berita = 2020
berita_dict, simpulan = crawl_berita('Jakarta', 'kekeringan', tahun_berita, 10)

# Menampilkan list berita dan link
print(f'Jumlah Berita: {len(berita_dict["judul"])}')
print(f'Simpulan: {simpulan}')
for i, judul in enumerate(berita_dict['judul']):
    print(f'{i + 1}. {judul}')
    print(f'   Link: {berita_dict["link"][i]}')
    print(f'   Deskripsi: {berita_dict["deskripsi"][i]}')
    print()
