import os
import re
import json
import math
from bs4 import BeautifulSoup
import time
import sqlite3
import sys


#DATA BASE INITIALATION BEGIN HERE


if os.path.exists('info.db'):
    conn = sqlite3.connect('info.db')
    conn.isolation_level = None
    print "Database connected successfully";
else:
    conn = sqlite3.connect('info.db')
    conn.isolation_level = None
    conn.execute('''
                CREATE TABLE WordsIndex
                (word char(255) NOT NULL,
                position char(255) NOT NULL,
                tf_idf real NOT NULL,
                head_rank real NOT NULL,
                ID INTEGER PRIMARY KEY AUTOINCREMENT);
                ''')
    conn.execute('''
                CREATE TABLE Positions_urls
                (position  NOT NULL,
                url char(255) NOT NULL);
                ''')
    print "Table created successfully";

#DATA BASE INITIALATION END HERE


file_bookkeeping = open("bookkeeping.json", 'r')
content_bookkeeping = file_bookkeeping.read()
urls = json.loads(content_bookkeeping)
simpleindex = {}
process = 0
processcount = 0
count = 0

for root, d, f in os.walk("../WEBPAGES_CLEAN/", topdown = False):
    #print f
    for name in f:
        processcount += 1
        if(processcount/3700>=1):
            process+=10
            print str(process) + "% done"
            processcount = 0
        path_pattern = os.path.join(root,name).split("/")
        path = path_pattern[len(path_pattern)-2]+"/"+path_pattern[len(path_pattern)-1]
        if(path_pattern[len(path_pattern)-1].isdigit()):
            count += 1
            #print urls[path]
            fp = open(os.path.join(root,name), 'r')
            unique_words = set()
            lines = fp.readlines()
            for line in lines:
                line = re.sub(r'\<.*?\>', " ", line)
                for word in re.sub(r'\W', " ", line).split():
                    word = word.lower()
                    if word.isalpha() and len(word)<50:
                        unique_words.add(word)

            for word in unique_words:
                if simpleindex.__contains__(word):
                    simpleindex[word] += 1
                    #simpleindex[word].append(path)
                else:
                    simpleindex[word] = 0
                    #simpleindex[word].append(path)
print "done"

def tag_ranking(html_doc):
    parttens = {}
    soup = BeautifulSoup(html_doc, "html.parser")
    soup.prettify()
    content_list = soup.find_all('title')
    for item in content_list:
        for word in item.getText().split():
            if parttens.__contains__(word):
                parttens[word] += 3
            else:
                parttens[word] = 3
    content_list = soup.find_all('h1')
    for item in content_list:
        for word in item.getText().split():
            if parttens.__contains__(word):
                parttens[word] += 2
            else:
                parttens[word] = 2
    content_list = soup.find_all('h2')
    for item in content_list:
        for word in item.getText().split():
            if parttens.__contains__(word):
                parttens[word] += 1
            else:
                parttens[word] = 1
    return parttens

fsw = open("stopwords.txt", 'r')
stopword_list = fsw.read().splitlines()

processcount = 0
process = 0
print "begin to update database:"
for root, d, f in os.walk("../WEBPAGES_CLEAN/", topdown = False):
    #print f
    for name in f:
        # processing count
        processcount += 1
        if(processcount/370>=1):
            process+=1
            print str(process) + "% done"
            processcount = 0
        # processing count end
        words_numbers = {}
        counter = 0
        path_patterns = os.path.join(root, name).split("/")
        #print path_patterns
        path = path_patterns[len(path_patterns) - 2] + "/" + path_patterns[len(path_patterns) - 1]
        #print path #position

        if(path_patterns[len(path_patterns)-1].isdigit()):
            fp = open(os.path.join(root,name), 'r')
            lines = fp.readlines()
            html_doc = "".join(lines)
            #until here html opened
            for line in lines:
                line = re.sub(r'\<.*?\>', " ", line)

                for word in re.sub(r'\W', " ", line).split():
                    word = word.lower()
                    if word.isalpha() and len(word)<50:
                        counter += 1
                        if words_numbers.__contains__(word):
                            words_numbers[word] += 1
                        else:
                            words_numbers[word] = 1
            #until here I got words and frenquncy in this document

            in_tags = tag_ranking(html_doc)
            #print in_tags
            #collect all datas
            #print counter

            for item in words_numbers:
                if not item in stopword_list:
                    tf = round(float(words_numbers[item])/counter, 4)
                    idf = round(float(math.log(float(37497) / words_numbers[item])), 4)
                    #result = item + " : TF: " + str(tf)
                    #result += " IDF: " + str(idf)
                    #result += " TF-IDF: "+ str(round(float(tf)*idf, 4))
                    tf_idf = round(float(tf)*idf, 4)
                else:
                    #result = item + " : TF-IDF: 0"
                    tf_idf = 0
                if in_tags.__contains__(item):
                    tag_rank = str(in_tags[item])
                else:
                    tag_rank = 0
                conn.execute("INSERT INTO WordsIndex (word,position,tf_idf,head_rank) \
                     VALUES ('"+str(item)+"','"+str(path)+"','"+str(tf_idf)+"','"+str(tag_rank)+"')");

            #time.sleep(2)

        #refer print round(float(13)/524,3)

print "index update completed:"

print "begin to update positions data:"
for item in urls:
    conn.execute("INSERT INTO Positions_urls (position,url) \
      VALUES ('"+str(item)+"','"+str(urls[item])+"')");
print "positions data update complete"
print "index database successfully created"




# parser.feed(content)
#      for line in fp:
#          for word in line.split():
#             parser = MyHTMLParser()
#               parser.feed(word)

 #count_list = sorted(count_dict.items(), key=lambda kv: (-kv[1], kv[0]))
            #for i in count_list:
            #    print(i[0], " - ", i[1])
