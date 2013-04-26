'''
Created on Mar 25, 2013

@author: darionascimento
'''

import urllib
import re
import sqlite3
from bs4 import BeautifulSoup

#News Parser:
#Download the news from newsletter website and parse them. Retrieves database and parse it to a new database
class newsParser:
    
    #Read from DB each entry with: url and Date
    def readFromDB(self,dbName):
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        for row in c.execute("Select * from feedsCrawling"):
            self.parseSite(row[0],row[1])
           
        
    def parseSite(self,url,date):
        fileURL = urllib.urlopen(url)
        
        domain = re.split("http://",url)[1]        
        domain = re.split("\.pt|\.com",domain)[0]
        
        doc = fileURL.read()        
        soup = BeautifulSoup(doc)
                
        if domain == "expresso.sapo":
            title = soup.select("#artigo")[0].h1.get_text()
            summary = soup.select("#artigo")[0].summary.get_text()
            article =  soup.select("#conteudo")[0].get_text()
                
        if domain == "feeds.dn":
            title = soup.select("#NewsTitle")[0].get_text()
            summary = soup.select("#NewsSummary")[0].get_text()
            article = soup.select("#Article")[0].get_text()
        
        
        if domain == "rss.feedsportal":
             title = soup.select("#NewsTitle")[0].get_text()
             summary = soup.select("#NewsSummary")[0].get_text()
             article = soup.select("#Article")[0].get_text()
        
        
        if domain == "economico.sapo":
             title = soup.select(".meta")[0].h2.get_text().decode("utf-8")
             summary = soup.select(".mainText")[0].strong.get_text().decode("utf-8")
             article = soup.select(".mainText")[0].get_text().decode("utf-8")
        
        if domain == "www.sol":
            title = soup.select("#NewsTitle")[0].get_text()
            summary = ""
            article = soup.select("#NewsSummary")[0].get_text()
        
        
        if domain == "www.rtp":
            title = soup.select("#video_detail")[0].h1.get_text()
            summary = ""
            article =  soup.select("#video_detail")[0].h2.get_text()
        

        
      #  print "title:"+title
      #  print "summary:"+summary 
      #  print "article:"+article   
      #  print "date: "+date    
        
newsParser().readFromDB("feeds.db")