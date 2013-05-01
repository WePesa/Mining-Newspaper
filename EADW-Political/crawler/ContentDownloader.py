'''
Created on Mar 25, 2013
'''
from threading import Thread
import urllib
import re
import sqlite3
import EntityExtraction
from bs4 import BeautifulSoup

#News Parser:
#Download the news from newsletter website and parse them. Retrieves database and parse it to a new database   
class ContentDownloader(Thread):
    
    def __init__(self,dbName):
        Thread.__init__(self)
        self.__dbName = dbName
      
    
    #Read from DB each entry with: url and Date
    def start(self):
        self.__conn = sqlite3.connect(self.__dbName)     
        cursor = self.__conn.cursor()   
        for row in cursor.execute("Select * from newsStorage where PROCESSED=0"):
                self.parseSite(row[0],row[1])        
        #self.printDatabase()
        
    def parseSite(self,url,date):
        print "parse new"
        fileURL = urllib.urlopen(url)
        
        domain = re.split("http://",url)[1]        
        domain = re.split("\.pt|\.com",domain)[0]
            
        doc = fileURL.read()        
        soup = BeautifulSoup(doc)
        try:
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
                title = soup.select(".meta")[0].h2.get_text()
                summary = soup.select(".mainText")[0].strong.get_text()
                article = soup.select(".mainText")[0].get_text()
            
            if domain == "www.sol":
                title = soup.select("#NewsTitle")[0].get_text()
                summary = ""
                article = soup.select("#NewsSummary")[0].get_text()
            
            
            if domain == "www.rtp":
                title = soup.select("#video_detail")[0].h1.get_text()
                summary = ""
                article =  soup.select("#video_detail")[0].h2.get_text()
            
            self.storeNew(url,date,domain,title,summary,article);
        except IndexError:
            print "IndexError: Ignore entry: "+url
        except UnboundLocalError:
            print "Invalid domain: "+url
        except: 
            print "Unexpected error: ignore entry:"+url
        
        #TODO send to whosh: Name tag etc
        EntityExtraction.ParseEntitiesFromDoc(article)
        
            
    def storeNew(self,url,date,domain,title,summary,article):
        print "Add new"
        cursor = self.__conn.cursor()
        cursor.execute('UPDATE newsStorage set DOMAIN=?, TITLE=?, SUMMARY=?, ARTICLE=? where url=?',(domain,title,summary,article,url))


ContentDownloader("news.db").start()
#   def printDatabase(self):
#      cursor = self.__conn.cursor()
#     for row in cursor.execute("Select * from newsStorage"):
#        print row
    #    self.__conn.commit()