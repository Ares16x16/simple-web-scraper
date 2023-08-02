import urllib.request
from html.parser import HTMLParser
import os

class HTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.headings = []
        self.paragraphs = []
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        if tag == 'a':
            href = next((v for k, v in attrs if k == 'href'), None)
            if href:
                self.links.append((self.get_starttag_text(), href))

    def handle_endtag(self, tag):
        self.current_tag = None

    def handle_data(self, data):
        if self.current_tag in ['h1', 'h2', 'h3']:
            self.headings.append(data.strip())
        elif self.current_tag == 'p':
            self.paragraphs.append(data.strip())

url = 'https://huggingface.co/'

with urllib.request.urlopen(url) as response:
    html = response.read().decode()
    
parser = HTMLParser()
parser.feed(html)

output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(os.path.join(output_dir, 'links.txt'), 'w', encoding='utf-8') as f:
    for link in parser.links:
        f.write(link[0] + ' (' + link[1] + ')\n')

with open(os.path.join(output_dir, 'headings.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(parser.headings))

with open(os.path.join(output_dir, 'paragraphs.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(parser.paragraphs))