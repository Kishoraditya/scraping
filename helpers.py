from bs4 import BeautifulSoup
import requests

def get_html_content(url):
    response = requests.get(url)
    html_content = response.text
    return html_content

def get_unique_class_names(soup2):
    elements_with_class = soup2.find_all(class_=True)
    class_groups = [tuple(element['class']) for element in elements_with_class]
    unique_class_groups = [', '.join(group) for group in set(class_groups)]
    unique_class_names = list(set(name for names_list in class_groups for name in names_list))
    return unique_class_groups, unique_class_names


def get_unique_tag_names(soup):
    elements_with_tag = soup.find_all(True)
    tag_names = [element.name for element in elements_with_tag]
    unique_tag_names = list(set(tag_names))
    return unique_tag_names

def get_unique_attribute_names(soup):
    attribute_names = set()
    for element in soup.find_all(True):
        attribute_names.update(list(element.attrs.keys()))
    unique_attribute_names = list(attribute_names)
    return unique_attribute_names

def get_scraped_data(html_content, target=None, attrs=None):
    soup = BeautifulSoup(html_content, 'html.parser')
    scraped_data = []

    if target:
        elements = soup.find_all(target, attrs=attrs)
        for element in elements:
            scraped_data.append({
                'class': element.get('class', []),
                # Add more key-value pairs if needed
            })

    return scraped_data
