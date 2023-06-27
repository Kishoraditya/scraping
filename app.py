from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        action = request.form['action']
        response = requests.get(url)
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')
        complete_html = soup.prettify()

        if action == 'scrape_names':
            html_tags = soup.find_all()
            css_tags = soup.find_all('style')
            js_tags = soup.find_all('script')
            
            elements_with_class = soup.find_all(class_=True)
            class_names = [element['class'] for element in elements_with_class]
            unique_class_names = []
            for names_list in class_names:
                for name in names_list:
                    if name not in unique_class_names:
                        unique_class_names.append(name)
            unique_class_names = list(unique_class_names)
            
            elements_with_tag = soup.find_all(True)
            tag_names = [element.name for element in elements_with_tag]
            unique_tag_names = []
            for names_list in tag_names:
                for name in names_list:
                    if name not in unique_tag_names:
                        unique_tag_names.append(name)
            unique_tag_names = list(unique_tag_names)
                    
            attribute_names = set()
            for element in soup.find_all(True):
                attribute_names.update(list(element.attrs.keys()))
            unique_attribute_names = []
            for names in attribute_names:
                if names not in unique_attribute_names:
                    unique_attribute_names.append(names)

            return render_template('index.html',class_names=unique_class_names, tag_names=unique_tag_names, attribute_names=unique_attribute_names, url=url, html_content=complete_html, html_tags=html_tags,
                                   css_tags=css_tags, js_tags=js_tags)

    return render_template('index.html')
@app.route('/scrape-class/<class_name>', methods=['GET'])
def scrape_class(class_name):
    url = request.args.get('url')  # Get the URL from the query parameters

    if url:
        response = requests.get(url)
        html_content = response.text
        

        soup = BeautifulSoup(html_content, 'html.parser')
        html_content = soup.prettify()
        # Find all elements with the specified class name
        elements_with_class = soup.find_all(class_=class_name)

        # Extract the desired data from the elements
        scraped_data = [element.text.strip() for element in elements_with_class]


        return render_template('scraped_data.html', html_content=html_content, class_name=class_name, data=scraped_data)

    return 'No URL provided.'

@app.route('/scrape-tag/<tag_name>', methods=['GET'])
def scrape_tag(tag_name):
    url = request.args.get('url')  # Get the URL from the query parameters

    if url:
        response = requests.get(url)
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all elements with the specified tag name
        elements_with_tag = soup.find_all(tag_name)

        # Extract the desired data from the elements
        scraped_data = [element.text.strip() for element in elements_with_tag]

        return render_template('scraped_data.html', html_content=html_content, class_name=tag_name, data=scraped_data)

    return 'No URL provided.'

@app.route('/scrape-attribute/<attribute_name>', methods=['GET'])
def scrape_attribute(attribute_name):
    url = request.args.get('url')  # Get the URL from the query parameters

    if url:
        response = requests.get(url)
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all elements with the specified attribute name
        elements_with_attribute = soup.find_all(attrs={attribute_name: True})

        # Extract the desired data from the elements
        scraped_data = [element.text.strip() for element in elements_with_attribute]

        return render_template('scraped_data.html', html_content=html_content, class_name=attribute_name,
                               data=scraped_data)

    return 'No URL provided.'

@app.route('/result', methods=['GET'])
def result():
    url = request.args.get('url')  # Get the URL from the query parameters

    if url:
        response = requests.get(url)
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')
        complete_html = soup.prettify()

        html_tags = soup.find_all()
        css_tags = soup.find_all('style')
        js_tags = soup.find_all('script')
        elements_with_class = soup.find_all(class_=True)
        class_names = [element['class'] for element in elements_with_class]
        unique_class_names = []
        for names_list in class_names:
            for name in names_list:
                if name not in unique_class_names:
                    unique_class_names.append(name)
        unique_class_names = list(unique_class_names)

        elements_with_tag = soup.find_all(True)
        tag_names = [element.name for element in elements_with_tag]
        unique_tag_names = []
        for names in tag_names:
            if names not in unique_tag_names:
                unique_tag_names.append(names)

        attribute_names = set()
        for element in soup.find_all(True):
            attribute_names.update(list(element.attrs.keys()))
        unique_attribute_names = list(attribute_names)

        return render_template('result.html', complete_html=complete_html, html_tags=html_tags,
                               css_tags=css_tags, js_tags=js_tags, class_names=unique_class_names,
                               tag_names=unique_tag_names, attribute_names=unique_attribute_names, url=url)

    return 'No URL provided.'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
