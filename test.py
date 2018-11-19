html_doc = """
<html><title>The Dormouse's story</title></head>

<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
Lacie</a> and
<h1>wew</h1>
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.
<h1>223</h1>
<p class="story">...</p>
"""
#{word,number}
import re
from decimal import *
import json
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, "html.parser")
in_tages = []
word_dict = {}
#soup.prettify()
print word_dict
print soup.title

slsls = soup.find_all('h1')
print slsls
for item in slsls:
    print item.getText()

file_bookkeeping = open("bookkeeping.json", 'r')
content_bookkeeping = file_bookkeeping.read()
urls = json.loads(content_bookkeeping)

for item in urls:
    print item
    print urls[item]

