# libraries
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

# native dependencies
import os
import time
from datetime import datetime, timedelta
import calendar
import re

GRAPH_PATH = '/html/body/div[3]/div/div/div[3]/div[2]/div/div[1]/div[2]'
NEXT_BUTTON_PATH = '/html/body/div[3]/div/div/div[3]/div[2]/div/div[1]/div[6]'
TOOLTIP_PATH = '/html/body/div[3]/div/div/div[3]/div[2]/div/div[1]/div[2]/div[67]'

driver = None

def init():
    global driver
    if 'DYNO' in os.environ:
        print '===============Heroku detected==============='
        driver = webdriver.PhantomJS(executable_path='bin/phantomjs')
        # driver = webdriver.Chrome(executable_path='bin/chromedriver')
    elif os.environ.get('OS', '') == 'Windows_NT':
        driver = webdriver.Chrome(executable_path='/cygdrive/c/Python27/Scripts/chromedriver.exe')
    else:
        driver = webdriver.Chrome(executable_path='bin/chromedriver')
        # driver = webdriver.PhantomJS(executable_path='drivers/phantomjs')

def fetch_all_data(f, t, days):
    current_date = time.strftime('%Y-%m-%d')
    future_date = (datetime.today() + timedelta(days=days)).strftime('%Y-%m-%d')

    start = time.time()
    data = {}
    url = build_url(f, t, current_date, future_date)
    driver.get(url)

    graph = wait_for_load(driver, GRAPH_PATH)       # select bar graph div
    next =  wait_for_load(driver, NEXT_BUTTON_PATH)     # select next button
    
    # return None indicating scraper error
    if next is None:
        return None

    for x in range(1):      # TODO: smarter loop than simple 6 iterations
        print 'Scraping loop' + str(x)
        fetch_data(graph, data, f, t)
        
        # Scroll to next button and mouse move to clear tooltip
        driver.execute_script("window.scrollTo("
            + str(next.location['x']) + "," + str(next.location['y']) + ")")
        result = None
        while result is None:
            try:
                move = ActionChains(driver).move_by_offset(100,100)
                move.perform()
                next.click()
                next.click()
                result = 1
            except:
                ActionChains(driver).move_by_offset(5,5)
                print 'Sleeping for click...'
                pass
                time.sleep(1)

        graph = wait_for_load(driver, GRAPH_PATH, 10)

    data = process_data(data)
    pprint(data)
    print("It took %s seconds" % (time.time() - start))

    return data

# Args: f=place from, t=place to
def fetch_data(graph, data, f, t):
    bars = graph.find_elements_by_xpath('div')[4:] # skip first 4 non data bars

    for bar in bars:
        hov = ActionChains(driver).move_to_element(bar)
        hov.perform()

        date = get_date(graph)
        timeout = 20
        while date == 'Loading...':  ## TODO: add a timeout
            if timeout <= 0:
                return
            else:
                time.sleep(0.5)
                timeout -= 1
                print 'Waiting for bars to load...'
                hov.perform()
                date = get_date(graph)
                
        if date != "No results found." and date not in data and date:
            # multiply unix timestamp by 1000 since highcharts is in ms
            timestamp = get_unix_timestamp(date) * 1000
            data[timestamp] = get_price(graph)

            print 'Scraped: ' + str(timestamp) + ' ' + str(date)

# processes the data by converting to array and sorting
def process_data(data):
    processed_data = []
    for time in data:
        processed_data.append([time, data[time]])
    # by default sorts according to processed_data[i][0] ascending
    processed_data.sort()

    return processed_data
        

# waits for AJAX bar graph to load, given # of tries and .3s delay between each
def wait_for_load(root, x_path, plural=False, tries=30, sleep=0.5, index=0):
    while tries > 0:
        try:
            if plural:
                elem = root.find_elements_by_xpath(x_path)[index]
            else:
                elem = root.find_element_by_xpath(x_path)
            print 'finding graph'
            print elem
            if elem.is_displayed():
                return elem
        except:
            pass
            print 'pass sleeping'
            tries -= 1
            time.sleep(sleep)
    return None

# Example: f=BOS, t=LAX, d=2014-07-02, r=2014-07-06
# URI component: f=BOS;t=CIA,FCO;d=2014-07-02;r=2014-07-06;mc=p
# mc=p shows the bar graph
def build_url(f, t, d, r):
    base_url = 'https://www.google.com/flights/#search;'
    params = ';'.join(['f=' + f, 't=' + t, 'd=' + d, 'r=' + r])
    return base_url + params + ';mc=p'

# extracts the departure date, adds the year
def get_date(graph):
    date = graph.find_elements_by_xpath(TOOLTIP_PATH + "/div")[1].get_attribute('innerText')
    if date == 'Loading...':
        return date
    elif len(date) > 19:
        current_month = datetime.now().month
        year = datetime.now().year
        if monthToNum(date.split()[1]) < current_month:
            year += 1
        print(date.split('-')[0] + str(year))
        return date.split('-')[0] + str(year)

# converts date string from get_date() to unix timestamp
def get_unix_timestamp(date_str):
    return calendar.timegm(datetime.strptime(date_str, '%a, %b %d %Y').timetuple())

# converts price string to int
def get_price(graph):
    price = graph.find_elements_by_xpath(TOOLTIP_PATH + "/div")[2].get_attribute('innerText')
    price = int(re.sub(r'[^0-9]', '', price))
    return price

def monthToNum(month):
    monthNum = {
                    'Jan' : 1,
                    'Feb' : 2,
                    'Mar' : 3,
                    'Apr' : 4,
                    'May' : 5,
                    'Jun' : 6,
                    'Jul' : 7,
                    'Aug' : 8,
                    'Sep' : 9, 
                    'Oct' : 10,
                    'Nov' : 11,
                    'Dec' : 12
            }
    return monthNum[month]