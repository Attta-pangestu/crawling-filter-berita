from helper import convert_date_filter_bing

date_start = "01/01/2018"
date_end = "01/01/2023"
keyword = "kemarau"

detik_pattern = {
    'search_elements': '//article[not(contains(@class, "video_tag"))]',
    'next_elements': '.paging a.last img[alt="Kanan"]',
    'description_elements': './/p',
    'date_elements': ".date",
    'link_elements': ".//a",
    'title_elements': ".title",
}

bing_pattern = {
    'search_elements': '//li[@class="b_algo"]',
    'next_elements': '.paging a.last img[alt="Kanan"]',
    'description_elements': './/p[@class="b_lineclamp4 b_algoSlug"]',
    'date_elements': ".news_dt",
    'link_elements': ".//h2/a",
    'title_elements': "a",
}

# Pemberian nama search engine harus sesuai dengan nama lembar di Google Sheets
search_engine_props = {
    # 'Detik': {
    #     'link': f"https://www.detik.com/search/searchall?query={keyword}&sortby=time&fromdatex={date_start}&todatex={date_end}&siteid=3",
    #     'pattern': detik_pattern,
    # },
    'Bing': {
        'link':
        f"https://www.bing.com/search?q=kekeringan&filters=ex1%3a%22ez5_{convert_date_filter_bing(date_start)}_19715%22",
        'pattern': bing_pattern,
    },
}


def generate_array_search():
  return [search_engine_props, keyword]


generate_array_search()
