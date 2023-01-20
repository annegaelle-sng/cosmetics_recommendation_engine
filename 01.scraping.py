"""
@author: annegaelle-sng
"""

# This is the part 1 of cosmetic recommendation: scraping cosmetic data from labelleboucle.com
# You can also download the csv file from same repository: cosmetic.csv

import time
import pandas as pd 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


driver = webdriver.Chrome()
driver.fullscreen_window() 

def scrollDown(driver, n_scroll):
    body = driver.find_element(By.TAG_NAME, "body")
    while n_scroll >= 0:
        body.send_keys(Keys.PAGE_DOWN)
        n_scroll -= 1
    return driver

#Part 1: get url for each products 
tickers = ['laver', 'soigner', 'coiffer']

df = pd.DataFrame(columns=['Label', 'URL'])

for ticker in tickers:
    url = 'https://labelleboucle.fr/collections/' + ticker 
    driver.get(url)
    numLinks = len(driver.find_elements(By.XPATH, "//div[@class='flex justify-center']/nav/ul[@class='flex items-center']/li"))
    subpageURL = []
    browser = scrollDown(driver, 10)
    time.sleep(10)
    for i in range(numLinks - 1):
          driver.get('https://labelleboucle.fr/collections/' + ticker + '?page=' + str(i +1))
          elements = driver.find_elements(By.XPATH, "//ul[@id='product-grid']/li[@class='w-1/2 py-3 px-2 mb-12 md:1/2 lg:w-1/3 xl:w-1/3']")
          browser = scrollDown(driver, 5)
          time.sleep(10)
          browser = scrollDown(driver, 10)
          time.sleep(10)
          for a in elements:
                subURL = a.find_element(By.TAG_NAME, 'a').get_attribute('href')
                subpageURL.append(subURL)

    # transform into a data frame
    dic = {'Label': ticker, 'URL': subpageURL}
    df = df.append(pd.DataFrame(dic), ignore_index = True)


print(df)
df.to_csv('datasets/url_cosmetic.csv', encoding = 'utf-8-sig', index = False)
 

#Part 2: scrap info for each products

df = pd.read_csv('datasets/url_cosmetic.csv')

# add columns
df2 = pd.DataFrame(columns=['brand', 'name', 'price', 'ingredients'])
df = pd.concat([df, df2], axis = 1)

for i in range(len(df)+1):
    url = df.URL[i]
    driver.get(url)
    time.sleep(5)
    
    #get brands and names
    df.brand[i] = driver.find_element(By.CSS_SELECTOR, '.hidden.mb-2.text-sm.md\:block.uppercase').text
    df.name[i] = driver.find_element(By.CSS_SELECTOR, '.mb-2.text-xl.font-extrabold.md\:block').text

    #get prices
    try:
        df.price[i] = driver.find_element(By.XPATH, "//div[@id='price-template--14595359211590__main']/span[@class='text-2xl font-bold']").text
    except NoSuchElementException:
        df.price[i] = 'No Info'

    browser = scrollDown(driver, 1)
    time.sleep(5)
    browser = scrollDown(driver, 1)
    time.sleep(5)

    #get ingredients
    try:
        xpath = "//tabs-buttons[@class='justify-center gap-4 mb-8']/div[@class='block transition-all border-0 border-black cursor-pointer selected:border-b-2 selected:font-bold'][3]"
        btn = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", btn)
        xpath2="//tabs-panels/div[@class='block mt-4']/div[@class='text-sm']/div"
        df.ingredients[i] = driver.find_element(By.XPATH, xpath2).text
    except NoSuchElementException:
        df.ingredients[i] = 'No Info'
    df.to_csv('datasets/cosmetic.csv', encoding = 'utf-8-sig', index = False)
    #control iteration
    print(i)

print(df)

df.to_csv('datasets/cosmetic.csv', encoding = 'utf-8-sig', index = False)