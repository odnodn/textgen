site = 'https://russian-dating.com/women?ageFrom=23;ageTo=33;hair=;eyes=;religion=;sort=upd;do=Search'

import selenium
from selenium import webdriver
import sys
from selenium.webdriver.common.keys import Keys


def login():
    idc = driver.find_element_by_name("id")
    password = driver.find_element_by_name("password")

    idc.send_keys("1229994")
    password.send_keys("4208361")
    password.send_keys(Keys.RETURN)

# Using Chrome to access web
driver = webdriver.Firefox()

# Open the website
driver.get(site)
driver.implicitly_wait(2)
#login()


elems =   driver.find_elements_by_xpath("//a[@href]")
hrefs = []

for elem in elems:
    #try:
        href = elem.get_attribute("href")
        if("profile" in href):
            hrefs.append(href)

login()

for href in hrefs:
    try:
        if("profile" in href):
            print (href)
            href = href.replace('profile', 'myChat')
            print(href)
            driver.get(href)
            #driver.get(href)
            driver.find_element_by_partial_link_text("Send").click()


            #driver.find_element_by_partial_link_text("Send").click()
            x = driver.find_element_by_name('body')
            x.send_keys("hi there, you are very pretty - kak dilla ")
            driver.find_element_by_tag_name('button').click();
    except:
        print ("Unexpected error:", sys.exc_info()[0])
        raise


driver.close()




