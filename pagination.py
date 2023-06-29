def paginate_elements(elements, page_size, current_page):
    total_elements = len(elements)
    total_pages = (total_elements + page_size - 1) // page_size
    current_page = min(max(current_page, 1), total_pages)

    start_index = (current_page - 1) * page_size
    end_index = start_index + page_size

    paginated_elements = elements[start_index:end_index]

    return paginated_elements, total_pages
