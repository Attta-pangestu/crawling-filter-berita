from helper import convert_date_filter_bing

date_start = "01/01/2018"
date_end = "01/01/2023"
keyword = "kemarau"


BING_SEARCH_URL = 'https://www.bing.com/search?q='

common_bing_pattern = {
    'search_results' : 'li.b_algo',
    'description_elements' : 'p.b_algoSlug', 
    'date_elements' : ".news_dt",
    'link_elements' : "h2 > a",
}

search_engine_props = {
    'antaranews' : {
        'domain' : 'antaranews.com', 
        'pattern' : common_bing_pattern, 
    },
    'detik' : {
        'domain' : 'detik.com', 
        'pattern' : common_bing_pattern, 
    },
    'tribunnews' : {
        'domain' : 'tribunnews.com', 
        'pattern' : common_bing_pattern, 
    },
    
}

def generate_array_search():
    search_interface = {}
    for key, search_prop in search_engine_props.items():
        search_link = f'{BING_SEARCH_URL}berita+{keyword}+{key}&filters=ex1%3a"ez5_{convert_date_filter_bing(date_start)}_{convert_date_filter_bing(date_end)}"'
        search_interface[key] = {
            'link': search_link,
            'pattern': search_prop['pattern'], 
            'domain' : search_prop['domain'], 
        }
    return [search_interface,keyword]

generate_array_search()


