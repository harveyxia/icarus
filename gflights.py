# from bs4 import BeautifulSoup
import time
import pdb
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome(executable_path='/cygdrive/c/Python27/Scripts/chromedriver.exe')
# driver = webdriver.PhantomJS(executable_path='/cygdrive/c/Python27/Scripts/phantomjs.exe')

GRAPH_PATH = '(//tbody)[2]/tr/td[2]/div/div[1]/div[4]/div[3]/div[2]/div[1]/div[2]'

def main(f, t):
    start = time.time()
    prices = {}
    url = build_url(f, t, '2014-07-02', '2014-07-06')
    driver.get(url)
    # select bar graph div
    graph = wait_for_load(driver, GRAPH_PATH, 10)
    # select next button
    next =  graph.find_elements_by_xpath('../*')[5]
    for x in range(6):      # TODO: smarter loop than simple 6 iterations
        get_prices(graph, prices, f, t)
        next.click()
        next.click()
        graph = wait_for_load(driver, GRAPH_PATH, 10)

    pprint(prices)
    print("It took %s seconds" % (time.time() - start))

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

# driver.get('https://www.google.com/flights/#search;f=BOS;t=CIA,FCO;d=2014-07-02;r=2014-07-06;mc=p')

# Args: f=place from, t=place to, d=departure date , r=return date
def get_prices(graph, prices, f, t):
    

    bars = graph.find_elements_by_xpath('./*')

    for bar in bars:
        hov = ActionChains(driver).move_to_element(bar)
        hov.perform()
        while date(graph) == 'Loading...':
            time.sleep(0.5)
            hov.perform()
        if date(graph) not in prices:
            prices[date(graph)] = price(graph)
        # print('Data: ' + date(graph) + ' ' + price(graph))

def date(graph):
    return graph.find_elements_by_xpath('./*[last()-1]/*')[0].get_attribute('innerText')

def price(graph):
    return graph.find_elements_by_xpath('./*[last()-1]/*')[1].get_attribute('innerText')

main('BOS', 'LAX')