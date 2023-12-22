date_start = "01/01/2018"
date_end = "01/01/2023"
keyword = "kemarau"

detik_pattern = {
    'description_elements' : './/p[@class="b_lineclamp4 b_algoSlug"]',
    'date_elements' : "news_dt",
    'link_elements' : ".//h2/a",
    'title_elements' : "title",
}

search_engine_props = {
    'detik' : {
        'link' : 'https://www.detik.com/search/searchall?query=', 
        'pattern' : detik_pattern, 
    },
    
}

def generate_array_search():
    search_interface = {}
    for key, search_prop in search_engine_props.items():
        search_link = f"{search_prop['link']}{keyword}&sortby=time&fromdatex={date_start}&todatex={date_end}&siteid=2"
        search_interface[key] = {
            'link': search_link,
            'pattern': search_prop['pattern']
        }
    return search_interface




