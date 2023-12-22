from search_with_pagination import search_with_pagination
from interface.link_interface import generate_array_search

# Inisiasi variabel

try: 
    # Dapatkan array pencarian dari antarmuka
    array_search = generate_array_search()

    # Iterasi melalui setiap elemen dalam array pencarian
    for source, data in array_search.items():
        link = data['link']
        element_pattern = data['pattern']

        # Panggil fungsi pencarian dengan paginasi
        links_metadata = search_with_pagination(link, element_pattern, num_pages=2)

except Exception as e:
    print(f"Terjadi error pada *scraping_link*: {e}")
