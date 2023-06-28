from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from helpers import get_html_content, get_unique_class_names, get_unique_tag_names, get_unique_attribute_names, get_scraped_data
import logging, io
from pagination import paginate_elements

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        action = request.form['action']
        html_content = get_html_content(url)
        log_messages = []  # List to store log messages
        log_handlers = app.logger.handlers  # Get the logger handlers

        soup = BeautifulSoup(html_content, 'html.parser')
        complete_html = soup.prettify()

        if action == 'scrape_names':
            unique_class_names = get_unique_class_names(soup)
            unique_tag_names = get_unique_tag_names(soup)
            unique_attribute_names = get_unique_attribute_names(soup)

            for handler in log_handlers:
                if isinstance(handler, logging.StreamHandler) and isinstance(handler.stream, io.TextIOBase):
                    try:
                        handler.stream.seek(0)  # Move the stream cursor to the beginning
                        log_content = handler.stream.read()
                        log_messages.extend(log_content.splitlines())
                    except (io.UnsupportedOperation, AttributeError):
                        log_messages.append("Encountered an unreadable stream")

            return render_template('index.html', class_names=unique_class_names, tag_names=unique_tag_names,
                                   attribute_names=unique_attribute_names, url=url, html_content=complete_html,
                                   html_tags=soup.find_all(), css_tags=soup.find_all('style'),
                                   js_tags=soup.find_all('script'), log_messages=log_messages)

    return render_template('index.html')


@app.route('/scrape-class/<class_name>', methods=['GET'])
def scrape_class(class_name):
    url = request.args.get('url')  # Get the URL from the query parameters
    page_size = int(request.args.get('page_size', default=10))
    
    if url:
        html_content = get_html_content(url)
        scraped_data = get_scraped_data(html_content, target=None, attrs={'class': class_name})
        
        # Pagination
        # Pagination
        page = request.args.get('page', default=1, type=int)
        paginated_data, total_pages = paginate_elements(scraped_data, page_size, page)

        return render_template('scraped_data.html', html_content=html_content, class_name=class_name,
                               data=paginated_data, total_pages=total_pages, current_page=page)

    return 'No URL provided.'


@app.route('/scrape-tag/<tag_name>', methods=['GET'])
def scrape_tag(tag_name):
    url = request.args.get('url')  # Get the URL from the query parameters
    page_size = int(request.args.get('page_size', default=10))

    if url:
        html_content = get_html_content(url)
        scraped_data = get_scraped_data(html_content, target=tag_name)
        # Pagination
        page = request.args.get('page', default=1, type=int)
        paginated_data, total_pages = paginate_elements(scraped_data, page_size, page)

        return render_template('scraped_data.html', html_content=html_content, class_name=tag_name,
                               data=paginated_data, total_pages=total_pages, current_page=page)

    return 'No URL provided.'


@app.route('/scrape-attribute/<attribute_name>', methods=['GET'])
def scrape_attribute(attribute_name):
    url = request.args.get('url')  # Get the URL from the query parameters
    page_size = int(request.args.get('page_size', default=10))

    if url:
        html_content = get_html_content(url)
        scraped_data = get_scraped_data(html_content, target=None, attrs={attribute_name: True})
        # Pagination
        page = request.args.get('page', default=1, type=int)
        paginated_data, total_pages = paginate_elements(scraped_data, page_size, page)

        return render_template('scraped_data.html', html_content=html_content, class_name=attribute_name,
                               data=paginated_data, total_pages=total_pages, current_page=page)

    return 'No URL provided.'


@app.route('/result', methods=['GET'])
def result():
    url = request.args.get('url')  # Get the URL from the query parameters

    if url:
        html_content = get_html_content(url)
        soup = BeautifulSoup(html_content, 'html.parser')
        complete_html = soup.prettify()
        unique_class_names = get_unique_class_names(soup)
        unique_tag_names = get_unique_tag_names(soup)
        unique_attribute_names = get_unique_attribute_names(soup)

        return render_template('result.html', complete_html=complete_html, html_tags=soup.find_all(),
                               css_tags=soup.find_all('style'), js_tags=soup.find_all('script'),
                               class_names=unique_class_names, tag_names=unique_tag_names,
                               attribute_names=unique_attribute_names, url=url)

    return 'No URL provided.'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
