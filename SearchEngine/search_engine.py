import json
import sqlite3

conn = sqlite3.connect('info.db')
conn.isolation_level = None
print "Database connected successfully";



class Searchengine():
    @staticmethod


    def retrive_signle_word(self,keyword):
        results = []
        cursor = conn.execute("select * from WordsIndex where word = '"+keyword+"' order by tf_idf desc LIMIT 10")
        for row in cursor:
            results.append(row[1])
        return results

    def retrive_two_words(self,keywords):
        results = []
        cursor = conn.execute("select * from WordsIndex where word = '"+keywords[0]+"' and position in (select position from WordsIndex where word = '"+keywords[0]+"' order by tf_idf desc limit 100) order by tf_idf desc limit 100; ")
        for row in cursor:
            results.append(row[1])
        return results

    def retrive_greater_two_words(self,keywords):
        results = []
        cursor = conn.execute("select * from WordsIndex where word = '"+keywords[0]+"' and position in (select position from WordsIndex where word = '"+keywords[0]+"' order by tf_idf desc limit 100) order by tf_idf desc limit 100; ")
        for row in cursor:
            results.append(row[1])
        return results

    @staticmethod
    def retrive(self, key_word):
        keywords = key_word.split(" ")
        results = []
        results_urls=[]
        if len(keywords) == 1:
            results = self.retrive_signle_word(self, keywords[0])

        elif len(keywords) == 2:
            results = self.retrive_two_words(self, keywords)

        elif len(keywords) > 2:
            results = self.retrive_greater_two_words(self, keywords)
        for item in results:
            cursor = conn.execute("select url from Positions_urls where position = '"+item+"'")
            for row in cursor:
                results_urls.append(row[0])
        return results_urls


SE = Searchengine()

while(1):

    words = raw_input("enter search words:")
    result = SE.retrive(SE,words)
    for item in results
        print item
