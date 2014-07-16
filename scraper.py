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

GRAPH_PATH = '(//tbody)[2]/tr/td[2]/div/div[1]/div[4]/div[3]/div[2]/div[1]/div[2]'

driver = 0

def init():
    global driver
    if 'DYNO' in os.environ:
        driver = webdriver.PhantomJS(executable_path='bin/phantomjs')
        print '===============Heroku detected==============='
        # driver = webdriver.PhantomJS(executable_path='bin/chromedriver')
    else:
        driver = webdriver.Chrome(executable_path='drivers/chromedriver')
        # driver = webdriver.PhantomJS(executable_path='drivers/phantomjs')
        # driver = webdriver.Chrome(executable_path='/cygdrive/c/Python27/Scripts/chromedriver.exe')
        # driver = webdriver.PhantomJS(executable_path='/cygdrive/c/Python27/Scripts/phantomjs.exe')
        driver.set_window_size(1024, 768)

def fetch_all_data(f, t, days):
    current_date = time.strftime('%Y-%m-%d')
    future_date = (datetime.today() + timedelta(days=days)).strftime('%Y-%m-%d')

    start = time.time()
    data = {}
    url = build_url(f, t, current_date, future_date)
    driver.get(url)

    graph = wait_for_load(driver, GRAPH_PATH, 10)       # select bar graph div
    next =  graph.find_elements_by_xpath('../*')[5]     # select next button

    for x in range(6):      # TODO: smarter loop than simple 6 iterations
        print 'Scraping loop' + str(x)
        fetch_data(graph, data, f, t)
        # next.click()
        # next.click()
        # Scroll to next button, to avoid unclickable error
        next_x = next.location['x']
        next_y = next.location['y']
        driver.execute_script("window.scrollTo(" + str(next_x) + "," + str(next_y) + ")")
        result = None
        while result is None:
            try:
                next.click()
                next.click()
                result = 1
            except:
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
    bars = graph.find_elements_by_xpath('./*')

    for bar in bars:
        hov = ActionChains(driver).move_to_element(bar)
        hov.perform()
        date = get_date(graph)
        while date == 'Loading...':  ## TODO: add a timeout
            time.sleep(0.5)
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
def wait_for_load(driver, x_path, tries):
    while tries:
        try:
            parent =  driver.find_element_by_xpath(x_path)
            if parent.is_displayed():
                return parent
        except:
            if tries <= 0:
                raise
        tries -= 1
        time.sleep(0.3)

# Example: f=BOS, t=LAX, d=2014-07-02, r=2014-07-06
# URI component: f=BOS;t=CIA,FCO;d=2014-07-02;r=2014-07-06;mc=p
# mc=p shows the bar graph
def build_url(f, t, d, r):
    base_url = 'https://www.google.com/flights/#search;'
    params = ';'.join(['f=' + f, 't=' + t, 'd=' + d, 'r=' + r])
    return base_url + params + ';mc=p'

# extracts the departure date, adds the year
def get_date(graph):
    date = graph.find_elements_by_xpath('./*[last()-1]/*')[0].get_attribute('innerText')
    if date == 'Loading...':
        return date
    elif len(date) > 19:
        current_month = datetime.now().month
        year = datetime.now().year
        if monthToNum(date.split()[1]) < current_month:
            year += 1

        return date.split('-')[0] + str(year)

# converts date string from get_date() to unix timestamp
def get_unix_timestamp(date_str):
    return calendar.timegm(datetime.strptime(date_str, '%a, %b %d %Y').timetuple())

# converts price string to int
def get_price(graph):
    price = graph.find_elements_by_xpath('./*[last()-1]/*')[1].get_attribute('innerText')
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