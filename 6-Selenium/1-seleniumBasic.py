from selenium import webdriver
import time

#driver = webdriver.PhantomJS(executable_path='/Users/ryan/Documents/git/python-crawling/6-Selenium/phantomjs/bin/phantomjs')
driver = webdriver.PhantomJS()
driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")
time.sleep(3)
print(driver.find_element_by_id("content").text)
