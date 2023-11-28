import requests
from bs4 import BeautifulSoup

def hitung_kemunculan_kata(url, kata_kunci_array):
    # Mendapatkan konten halaman web
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Mendapatkan teks dari halaman web
    teks = soup.get_text()

    # Inisialisasi dictionary untuk menyimpan jumlah kemunculan kata kunci
    find_kabupaten = {}

    # Iterasi melalui setiap kata kunci
    for kata_kunci in kata_kunci_array:
        # Menghitung kemunculan kata kunci
        kemunculan = teks.lower().count(kata_kunci.lower())
        
        # Jika ditemukan, menyimpan jumlah kemunculan
        if kemunculan > 0:
            key = f'keyword {kata_kunci}'
            if key in find_kabupaten:
                find_kabupaten[key] += kemunculan
            else:
                find_kabupaten[key] = kemunculan

    return find_kabupaten

# List link berita
links = [
    "https://regional.kompas.com/read/2022/10/11/083314478/3-wilayah-di-ntt-masih-alami-kekeringan-ekstrem-terpanjang-205-hari-tanpa-hujan",
    "https://voaindonesia.com/a/ntb-dan-ntt-hadapi-bencana-kekeringan/6212316.html",
    "https://bpbd.nttprov.go.id/berita/detail/240/NTT-Masuk-Puncak-Musim-Kemarau",
    "https://www.antaranews.com/berita/971750/kekeringan-bukan-lagi-bencana-bagi-ntt",
    "https://ntt.bps.go.id/indicator/27/913/1/korban-kekeringan-jiwa-2020-2022",
    "https://www.mongabay.co.id/2021/07/25/ancaman-kekeringan-melanda-ntt-apa-yang-harus-dilakukan/",
    "https://www.liputan6.com/news/read/4647287/bmkg-kekeringan-ekstrem-dan-hari-tanpa-hujan-hanya-terjadi-di-ntt",
    "https://news.republika.co.id/berita/rh3lxo382/enam-wilayah-ntt-terancam-bencana-kekeringan",
    "https://blog.insanbumimandiri.org/ntt-provinsi-nomor-1-kekeringan-terparah-se-indonesia/",
    "https://news.detik.com/berita/3047262/ntt-7-kabupaten-berstatus-awas-bencana-kekeringan",
    "https://www.merdeka.com/peristiwa/11-daerah-di-ntt-alami-kekeringan-ekstrem-panjang.html",
    "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8055416/",
    "https://jsi.universitaspertamina.ac.id/jsi/article/view/4",
    "https://airkami.id/provinsi-ntb-dan-ntt-hadapi-bencana-kekeringan/",
    "https://data.pu.go.id/infografis/waspada-potensi-kekeringan-di-ntt-bulan-november-2020",
    "https://www.cnnindonesia.com/teknologi/20190625181723199-406356/jakarta-hingga-ntt-berpotensi-kekeringan-jelang-musim-kemarau",
    "https://mediaindonesia.com/nusantara/439731/lima-kabupaten-di-ntt-berstatus-awas-kekeringan",
    "https://rakyatntt.com/ntt-hadapi-bencana-kekeringan-ini-solusi-yang-ditawarkan-dprd-ntt/",
    "https://www.cnbcindonesia.com/news/202007262005164175509/waspada-4-wilayah-di-ri-terancam-kekeringan-ekstrem",
    "https://ntt.pikiran-rakyat.com/regional/pr-2324411948/ancaman-kekeringan-di-ntt-bpbd-imbau-petani-hemat-air-dengan-cara-ini",
    "https://www.jawapos.com/berita-sekitar-anda/01281858/sembilan-kabupaten-di-ntt-berstatus-waspada-kekeringan-meteorologis",
]

# Array kata kunci
kata_kunci_array = ['Lombok Barat', 'Lombok Tengah', 'Lombok Timur', 'Sumbawa', 'Dompu', 'Bima',
                    'Sumbawa Barat', 'Lombok Utara', 'Mataram', 'Kota Bima']

# Inisialisasi dictionary untuk menyimpan hasil kumulatif
hasil_kumulatif = {}

# Iterasi melalui setiap link berita
for link in links:
    hasil_kemunculan = hitung_kemunculan_kata(link, kata_kunci_array)
    
    # Menambahkan hasil pencarian dari link berita ke hasil kumulatif
    for kata_kunci, kemunculan in hasil_kemunculan.items():
        if kata_kunci in hasil_kumulatif:
            hasil_kumulatif[kata_kunci] += kemunculan
        else:
            hasil_kumulatif[kata_kunci] = kemunculan

# Menampilkan hasil kumulatif
print('Hasil Kumulatif Kemunculan Kata Kunci:')
for kata_kunci, kemunculan in hasil_kumulatif.items():
    print(f'{kata_kunci} : {kemunculan} kali')
