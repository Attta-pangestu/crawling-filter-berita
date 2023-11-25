import requests
from bs4 import BeautifulSoup
import re

def google_search(query, year=None):
    search_url = f"https://www.google.com/search?q={query}"
    
    if year:
        # Menambahkan filter tahun ke dalam query
        search_url += f"&tbs=cdr:1,cd_min:{year},cd_max:{year}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve search results. Status code: {response.status_code}")
        return None

def extract_links_and_titles(html):
    soup = BeautifulSoup(html, 'html.parser')
    search_results = soup.find_all('div', class_='tF2Cxc')

    results_array = []
    for result in search_results:
        link = result.find('a')['href']
        title = result.find('h3').get_text()
        results_array.append({'title': title, 'link': link})

    return results_array

def main():
    search_query = input("Masukkan query pencarian: ")
    search_year = input("Masukkan tahun filter (opsional): ")

    if search_year and not re.match(r'^\d{4}$', search_year):
        print("Format tahun tidak valid. Gunakan format YYYY (contoh: 2022)")
        return

    search_html = google_search(search_query, search_year)

    if search_html:
        search_results = extract_links_and_titles(search_html)

        print("\nHasil Pencarian:")
        for i, result in enumerate(search_results, 1):
            print(f"{i}. {result['title']} - {result['link']}")

if __name__ == "__main__":
    main()
