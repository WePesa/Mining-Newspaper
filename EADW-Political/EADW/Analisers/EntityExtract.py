#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import floresta
from pprint import pprint
from  EADW.Analisers import WordProcessor
import sqlite3
import re
import unicodedata
import string
from collections import Counter
from TAGAnalizer import TAGAnalizer
from OpinionAnalysis import Opinion
#Ler cada um dos textos nao processados
#Realizar a analise com o NLTK


class EntityExtractor:
    
    __dBLexiconLocation = "../storage/lexicon.db"
    lixo  = nltk.corpus.stopwords.words('portuguese')
    opinionAnalist = Opinion()
    tagger = TAGAnalizer()
    IgnoreFile = "Utils/SentimentsBase/in/IgnoreNamesTrainingSet.txt"

    ########################################################
    #Load rubish names list and init properNameProcessor
    #########################################################
    def __init__(self):
        self.ProperNameProcessor = WordProcessor.ProperNameProcessor()
        self.LoadIgnoreList(self.IgnoreFile)#Adiciona a lista "lixo" palavras geradas pelo traning set
        #conn = sqlite3.connect(self.__dBLexiconLocation)
        #cursor = conn.cursor()
        #self.rubishProperNounList = []
        #for row in cursor.execute("Select * from rubishNames"):
        #    self.rubishProperNounList.append(row[0]) 
        #conn.close()
        
    def LoadIgnoreList(self,IgnoreFilePath):
        fd = open(IgnoreFilePath, "r")
        list = fd.read().split(":")
        print "Loaded ignore list\n"
        self.lixo += list
    
    def strip_punctuation(self,text):
        punctutation_cats = set(['Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po'])
        return ''.join(x for x in text if unicodedata.category(x) not in punctutation_cats)
    
    ########################################################
    #Parse the doc, get entities, analysis etc
    ########################################################
    def ParseEntitiesFromDoc(self,url,doc):
        
        self.ProperNameProcessor.init()
        results = dict()
        sentences = nltk.sent_tokenize(doc.decode("utf8"))
                    
        for sentence in sentences:
            sentence = self.strip_punctuation(sentence)
            words = sentence.split(" ")
            for word in words:
                #retira lixo
                if(len(word) < 2):
                    continue
                
                # verifica se pretence a lista de stop words
                if(word.lower() in self.lixo):
                    continue
                
                POS = self.tagger.getTagFromBD(word)
            
                if  POS == 'NPROP': 
                    #its properNoun
                    self.ProperNameProcessor.updateNewName(word,True) 
                else:
                    self.ProperNameProcessor.updateNewName(word,False) 
            
            #contar o numero de ocorrencias
            #associar o feeling da frase a esta entidade
            entities = self.ProperNameProcessor.doFinal()
            counting = Counter(entities.values())
            
            feelingAndAbjectives = self.opinionAnalist.getSentenceOpinion(sentence)
            feeling = feelingAndAbjectives[0]
            adjectives = feelingAndAbjectives[1]
            # TODO Dario Usar os Ajectivos
            
            # Somar ocorrencias e sentimento da frase
            for (entity,appears) in counting.items():
                if entity not in results:
                    results[entity] = [appears,feeling]
                    print entity, feeling
                else:
                    results[entity][0] += appears
                    results[entity][1] += feeling
            
        return results
   
   
   
   
    
    
    
    
    
    
    


