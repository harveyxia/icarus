# from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome(executable_path='/cygdrive/c/Python27/Scripts/chromedriver.exe')

driver.get('https://www.google.com/flights/#search;f=BOS;t=CIA,FCO;d=2014-07-02;r=2014-07-06;mc=p')

def wait_for_load(driver, selector, tries):
    while tries:
        try:
            elem = driver.find_element_by_class_name('GLVBGF1HWC')
            if elem.is_displayed():
                return elem
        except Exception as exception:
            if tries <= 0:
                raise exception
        tries -= 1
        time.sleep(0.3)

# elem = wait_for_load(driver.find_element_by_class_name('GLVBGF1HWC'))
elem = wait_for_load(driver, 'GLVBGF1HWC', 10)

# children = elem.find_elements_by_xpath('./*')
children = elem.find_elements_by_css_selector(' .GLVBGF1BXC')

for child in children:
    hov = ActionChains(driver).move_to_element(child)
    hov.perform()
    while driver.find_element_by_class_name('GLVBGF1IXC').text == 'Loading...':
        time.sleep(1)
    hov.perform()
    print('Data: ' + driver.find_element_by_class_name('GLVBGF1IXC').text + ' ' + driver.find_element_by_class_name('GLVBGF1JXC').text)

# try:
#     elem = driver.find_element_by_class_name('doesnt exist')
# except Exception as exception:
#     print exception.__class__.__name__