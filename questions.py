
import json
import re
import logging
# Web scraping, pickle imports
import requests
from bs4 import BeautifulSoup
import pickle
import scrapy
from scrapy.http.request import Request


class conversation(object):
    def __init__(self,name,content):

        self.name = name
        self.content = content
    def __str__(self):
        return 'Conversation titled: '+self.name


# # Scrapes transcript data from scrapsfromtheloft.com
# def url_to_transcript(url):
def batch(url):
    '''
     A batch consists of 5 conversations
    '''
    res = []
    page = requests.get(url).text
    soup = BeautifulSoup(page, "lxml")
    print('Extracting page: '+str(url))
    for e in soup.find_all("a",{"class":"hsp-card-episode"}):        
        element_text = e.find_all('h3')[0].text        
        if e.has_key('href'):
            element_url = 'https://www.happyscribe.com'+e['href']  
            transcript = BeautifulSoup(requests.get(element_url).text)
            content = ''.join([x.text for x in transcript.find_all('p',{"class":"hsp-paragraph-words"})])
            
            res.append(conversation(element_text,content))
    return res    
    
        
def extract_all(debug=False):    
    total = []
    i = 0
    while True:    
        url = 'https://www.happyscribe.com/public/lex-fridman-podcast-artificial-intelligence-ai?_=1605486671297&page={}&sort=popular'.format(str(i))        
        i += 1
        local_batch = batch(url)
        if len(local_batch) == 0:break
        total.append(batch(url))
    return total

def save_data(data):
    with open('results.csv','w+') as file:
        for batch in data:
            for i in batch:        
                file.write(i.name+','+i.content+'\n')
    
all_conversations = extract_all(debug=True)
save_data(all_conversations)

# l = [e.find_all('h3')[0].text for e in soup.find_all("div",{"class":"hsp-card-episode-info"})]
# text = [p.text for p in soup.find(class_="hsp-card-episode-info").find_all('h3')]    



# url = 
# res = url_to_transcript(url)
# print(res)