import math

def calc_pages(data, per_page, page):
    total_pages = math.ceil((len(data) / per_page))
    start_index = per_page * (page -1)
    end_index = start_index + per_page
    page_data = data[start_index:end_index]

    return total_pages, page, page_data