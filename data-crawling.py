import requests
from bs4 import BeautifulSoup
import re

def google_search(query, year_range=None, num_pages=5):
    query = query.replace(" ", "+")
    results_array = []

    for page in range(num_pages):
        start_index = page * 10
        search_url = f"https://www.google.com/search?q={query}&start={start_index}"

        if year_range:
            search_url += f"&tbs=cdr:1,cd_min:{year_range[0]},cd_max:{year_range[1]}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(search_url, headers=headers)
        if response.status_code == 200:
            search_results = extract_links_and_titles(response.text)
            results_array.extend(search_results)
        else:
            print(f"Failed to retrieve search results on page {page + 1}. Status code: {response.status_code}")

    return results_array

def extract_links_and_titles(html):
    soup = BeautifulSoup(html, 'html.parser')
    search_results = soup.find_all('div', class_='tF2Cxc')

    results_array = []
    for result in search_results:
        link = result.find('a')['href']
        title = result.find('h3').get_text()
        results_array.append({'title': title, 'link': link})

    return results_array

def analyze_news_articles(news_articles):
    kabupaten_count = {}
    desa_count = {}

    for article in news_articles:
        title = article['title'].lower()

        if 'kabupaten' in title:
            kabupaten_name = re.search(r'kabupaten (\w+)', title)
            if kabupaten_name:
                kabupaten_name = kabupaten_name.group(1)
                kabupaten_count[kabupaten_name] = kabupaten_count.get(kabupaten_name, 0) + 1

        if 'desa' in title:
            desa_name = re.search(r'desa (\w+)', title)
            if desa_name:
                desa_name = desa_name.group(1)
                desa_count[desa_name] = desa_count.get(desa_name, 0) + 1

    return kabupaten_count, desa_count

def main():
    search_query = input("Masukkan query pencarian (lebih dari satu kalimat): ")
    start_year = input("Masukkan tahun awal filter: ")
    end_year = input("Masukkan tahun akhir filter: ")

    if not re.match(r'^\d{4}$', start_year) or not re.match(r'^\d{4}$', end_year):
        print("Format tahun tidak valid. Gunakan format YYYY (contoh: 2020)")
        return

    year_range = (start_year, end_year)

    num_pages = int(input("Masukkan jumlah halaman hasil pencarian yang ingin diambil: "))

    search_results = google_search(search_query, year_range, num_pages)

    if search_results:
        print("\nHasil Pencarian:")
        for i, result in enumerate(search_results, 1):
            print(f"{i}. {result['title']} - {result['link']}")

        kabupaten_count, desa_count = analyze_news_articles(search_results)

        print("\nAnalisis Berita:")
        print("\nKabupaten:")
        for kabupaten, count in kabupaten_count.items():
            print(f"{kabupaten}: {count} kali disebut")

        print("\nDesa:")
        for desa, count in desa_count.items():
            print(f"{desa}: {count} kali disebut")

if __name__ == "__main__":
    main()
