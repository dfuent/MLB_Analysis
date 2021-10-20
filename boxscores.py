# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 10:12:57 2020

Presidential and Vice Presidential Debate scraper

"""
from bs4 import BeautifulSoup, SoupStrainer
from urllib.request import Request, urlopen
import pandas as pd
import time
import io
from selenium import webdriver
from ftfy import fix_encoding
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Option so that selenium doesn't open a new Chrome window
options = webdriver.ChromeOptions()
options.add_argument('--headless')

t_0 = time.time()

# input headers to bypass issue loading transcript site


# URL base

old_links = pd.read_csv('bs_links.csv')
old_links =old_links['link'].tolist()

#%%

l = ['2020-schedule.shtml']

d = ['2020-09-30-0',
'2020-09-30-0',
'2020-06-30-0',
'2020-03-31-0',
'2019-12-31-0',
'2019-09-30-0',
'2019-06-30-0',
'2019-03-31-0',
'2018-12-31-0',
'2018-09-30-0',
'2018-06-30-0',
'2018-03-31-0',
'2017-12-31-0',
'2017-09-30-0',
'2017-06-30-0',
'2017-03-31-0',
'2016-12-31-0',
'2016-09-30-0',
'2016-06-30-0',
'2016-03-31-0',
'2015-12-31-0',
'2015-09-30-0',
'2015-06-30-0',
'2015-03-31-0',
'2014-12-31-0',
'2014-09-30-0',
'2014-06-30-0',
'2014-03-31-0',
'2013-12-31-0',
'2013-09-30-0',
'2013-06-30-0',
'2013-03-31-0',
'2012-12-31-0',
'2012-09-30-0',
'2012-06-30-0',
'2012-03-31-0',
'2011-12-31-0',
'2011-09-30-0',
'2011-06-30-0',
'2011-03-31-0']


df = pd.DataFrame()

r = 26

m = 0
n = 0

hd = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    

# initiate web driver for Chrome
driver = webdriver.Chrome(options=options)

for j in range(5):
    
    m += 1
    
    print('Link number ' + str(m))
    
    root = 'https://www.baseball-reference.com/leagues/MLB/' + str(2020 - j) + '-schedule.shtml'
    
    req = Request(root)
    
    # read site
    
    html_page = urlopen(req).read()
    
    # create HTML "soup"
    
    soup = BeautifulSoup(html_page, "lxml")

    
    #use driver to open url
    driver.get(root)
    
    
    links = []
    for link in soup.findAll('a'):
        links.append(str(link.get('href')))
    
    t = [k for k in links if 'boxes' in k and k not in old_links and 'boxes/?date' not in k]
    #t = [i for i in links if i not in old_links]
    
    
    t = list(set(t))
    
    print(t)
    print(len(t))
    
    tot = len(t)
    n= 0
    
    for i in t:
        
        n+=1
        print(str(n) + ' of ' + str(tot))
        
        #print('Date ' + i)
        
        loop_time = time.time()
        
        root = 'https://www.baseball-reference.com/' + str(i)
        
        # send request to site with headers to bypass Forbidden issue
        req = Request(root)
        
        driver.get(root)
        
        #print(req)
        
        #print(root)
        
        # read site
        
        table_k = pd.DataFrame()
        
        try:
            
        
            html_page = urlopen(req).read()
            
            driver.implicitly_wait(10)
    
            
            # create HTML "soup"
            html=driver.page_source
            soup=BeautifulSoup(html,'lxml')
            
            #print(soup)
        
            tableHTML=soup.findAll("div", {"class": "table_container is_setup"})
            
            #print(tableHTML)
            
            for table in tableHTML:
                
                print(table.get('id'))
                
                table_temp = pd.DataFrame()
                
                table_temp=table_temp.append(pd.DataFrame(pd.read_html(str(table))[0]))
                table_temp['table_name'] = table.get('id')
                table_k = table_k.append(table_temp)
            
            print(i)
            table_k['link'] = i
            #table_k['date'] = i
            
            df= df.append(table_k)
            
            
            df = df.loc[df['Batting'] != 'Team Totals']
            df = df.loc[df['table_name'] != 'div_play_by_play']
            df = df.loc[df['table_name'] != 'div_top_plays']
            df = df[~df.table_name.str.contains("standings")]
            
            
            #print('Fund finished in {0: .2f} seconds'.format(time.time()-t_0))
    
            df.to_csv('box_scores.csv', index = False)
    
        except:
            pass
        
        
        print('Finished game in {0: .2f} seconds'.format(time.time()-loop_time))
        print('Total time {0: .2f} seconds\n'.format(time.time()-t_0))
    
    print('Finished season. Total time is {0: .2f} seconds'.format(time.time()-t_0))
    
#print('{0} loops for {1} took {2: .2f} seconds.'.format(l, h, time.time()-loop_time))

 
    ######################################     

#df = pd.DataFrame(fin_list, columns = ['Line Count', 'Debate', 'Speaker', 'Transcript'])
#df.to_csv('Transcripts_df.csv', index = False)    
    
print('Finished in {0: .2f} seconds'.format(time.time()-t_0))

timestr = time.strftime("%Y%m%d-%H%M%S")

df.to_csv('boxscores_hit' + timestr + '.csv')




#%%
