from search_with_pagination import search_with_pagination
from link_interface import generate_array_search

# Inisiasi variabel

try: 
    # Dapatkan array pencarian dari antarmuka
    interprete_interface = generate_array_search()
    search_interface = interprete_interface[0]
    keyword = interprete_interface[1]
    

    # Iterasi melalui setiap elemen dalam array pencarian
    for source, data in search_interface.items():
        link = data['link']
        element_pattern = data['pattern']
        domain = data['domain'] 

        print("============================================")
        print("MEMULAI SCRAPING DARI MEDIA ", source)
        print("============================================\n")
        
        # Panggil fungsi pencarian dengan paginasi
        links_metadata = search_with_pagination(keyword,link, element_pattern, domain,  num_pages=2)

except Exception as e:
    print(f"Terjadi error pada *scraping_link*: {e}")
