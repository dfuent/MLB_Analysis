''' 
CS 5010: Homework 3: Python and Web Scraper

by David Fuentes (dmf4ns) & Dylan Howe (dsh7pd)

Data scraped from BaseballReference.com

'''

# function to produce Baseball Reference data. Function returns a tuple
# of file names -- one for batting and one for pitching data -- to which
# the data were written

def yearly_baseball_stats(fin_year = 2020, n_years = 10): # set reasonable defaults
    
    #dependencies and imports
    import pandas as pd
    import time
    from selenium import webdriver
    from bs4 import BeautifulSoup
    

    
    
    t_1 = time.time() # will use to time parts of the function


    # Option so that selenium doesn't open a new Chrome window
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    
    #initiate web driver
    driver = webdriver.Chrome(options=options)    
    
    # create empty DBs to which we'll append data    
    table_bat = pd.DataFrame()
    table_pitch = pd.DataFrame()
    
    # start a loop. we will create one pitching and one batting DF per year, 
    # then append to their respective aggregate DFs created above
    
    for i in range(n_years): # run once per inputted year
        
        loop_time = time.time() # will use to show some time info
        table_i = pd.DataFrame() # empty batting DF
        table_p = pd.DataFrame() # empty pitching DF
        
        print('Year = {0}'.format(fin_year - i)) # show the user the current iteration
        
        # set respective URLs for Baseball Reference data; one for batting data, one for pitching
        url_b = 'https://www.baseball-reference.com/leagues/MLB/'+str(fin_year - i)+'-standard-batting.shtml'
        url_p = 'https://www.baseball-reference.com/leagues/MLB/'+str(fin_year - i)+'-standard-pitching.shtml'      

        #use driver to open batting url
        driver.get(url_b)
        
        #wait three seconds to load page (probably not necessary)
        time.sleep(3)
        
        #extract page HTML and parse with BeautifulSoup
        html=driver.page_source
        soup=BeautifulSoup(html,'html.parser')
        
        #find the table with batter statistics by its ID
        tableHTML=soup.find(id="players_standard_batting")
        
        #use pandas to read the table into a DataFrame
        table_i=table_i.append(pd.DataFrame(pd.read_html(str(tableHTML))[0]))      
        
        # add columns with some helpful info, like year and position (batter/pitcher)
        table_i['Year'] = fin_year - i   
        table_i['Pos'] = 'Batter'
        
        # cleanup some encoding issues with the names
        clean_names = []
        for name in table_i['Name']:
            name = name.replace('*', '')
            name = name.replace('#', '')
            name = name.replace('+', '')
            name = name.replace('\xa0', ' ')
            clean_names.append(name)
        table_i['Name'] = clean_names        
        
        # append the year's batting data to the aggregate DF and print info for
        # the user
        table_bat = table_bat.append(table_i)
        print('Cumulative size of data table: {0} rows'.format(table_bat['Name'].count()))
        print('Year {0} Batting loop took {1: .4f} seconds'.format(fin_year - i, time.time()-loop_time))
        
        # repeat the process for the pitching data:        
        time_p = time.time()
        
        #use driver to open url
        driver.get(url_p)
        
        #wait three seconds to load page (probably not necessary)
        time.sleep(3)
        
        #extract page HTML and parse with BeautifulSoup
        html=driver.page_source
        soup=BeautifulSoup(html,'html.parser')
        
        #find the table with pitching statistics by its ID
        tableHTML=soup.find(id="players_standard_pitching")
        
        #use pandas to read the table into a DataFrame
        table_p=table_p.append(pd.DataFrame(pd.read_html(str(tableHTML))[0]))      
        
        # add the new columns again with the data year and pitching
        table_p['Year'] = fin_year - i   
        table_p['Pos'] = 'Pitching'
        
        # clean up name encoding
        clean_names = []
        for name in table_p['Name']:
            name = name.replace('*', '')
            name = name.replace('#', '')
            name = name.replace('+', '')
            name = name.replace('\xa0', ' ')
            clean_names.append(name)
        table_p['Name'] = clean_names
        
        # append data and give user some info, like how long the pitching data pull took
        table_pitch = table_pitch.append(table_p)
        print('Cumulative size of data table: {0} rows'.format(table_pitch['Name'].count()))
        print('Year {0} Pitching loop took {1: .4f} seconds'.format(fin_year - i, time.time()-time_p))
    
    #Right now there are headers every 25 rows in the table (Rk = Rk in these rows), 
    #remove the intermittent headers
    table_pitch = table_pitch[table_pitch['Rk'] != 'Rk']
    table_bat = table_bat[table_bat['Rk'] != 'Rk']
    
    # there are instances where a player swaps leagues during the season. 
    # Tm = MLB is their agg line, but they already show up twice disaggregated,
    # so we should remove
    table_pitch = table_pitch[table_pitch['Lg'] != 'MLB'] 
    table_bat = table_bat[table_bat['Lg'] != 'MLB']
    
    #Right now there's a summary row at the bottom, remove it
    table_pitch = table_pitch[table_pitch['Name'] != 'LgAvg per 180 IP']
    table_bat = table_bat[table_bat['Name'] != 'LgAvg per 600 PA']
    
    #set the index
    table_pitch = table_pitch.reset_index().drop(columns='index')
    table_bat = table_bat.reset_index().drop(columns='index')  
           
    print('Time check before export: {0: .4f}'.format(time.time()-t_1))
 
    # export each table to CSV files
    table_pitch.to_csv('br_table_pitch' + str(fin_year - (n_years-1)) +'_to_'+str(fin_year) + '.csv', index = False)
    table_bat.to_csv('br_table_bat' + str(fin_year - (n_years-1)) +'_to_'+str(fin_year) + '.csv', index = False)
   
    print('Tables saved. Total time: {0: .4f}s'.format(time.time()-t_1))
    
    # return tuple of file names
    return ('br_table_pitch' + str(fin_year - (n_years-1)) +'_to_'+str(fin_year) + '.csv', 'br_table_bat' 
            + str(fin_year - (n_years-1)) +'_to_'+str(fin_year) + '.csv')
        

file_p, file_b = yearly_baseball_stats(2020, 26) # run our file back to 1995


