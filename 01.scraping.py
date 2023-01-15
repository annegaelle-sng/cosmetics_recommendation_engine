"""
@author: annegaelle-sng
"""

# This is the part 1 of cosmetic recommendation: scraping cosmetic data from labelleboucle.com
# You can also daownload the csv file from same repository: cosmetic.csv

import time
import pandas as pd 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

chrome_path = '/Users/anne-gaellesongeons/Downloads/chromedriver_mac64'

driver = webdriver.Chrome()
driver.fullscreen_window() 

def scrollDown(driver, n_scroll):
    body = driver.find_element(By.TAG_NAME, "body")
    while n_scroll >= 0:
        body.send_keys(Keys.PAGE_DOWN)
        n_scroll -= 1
    return driver

tickers = ['laver', 'soigner', 'coiffer']

# df = pd.DataFrame(columns=['Label', 'URL'])

# for ticker in tickers:
#     url = 'https://labelleboucle.fr/collections/' + ticker 
#     driver.get(url)
#     numLinks = len(driver.find_elements(By.XPATH, "//div[@class='flex justify-center']/nav/ul[@class='flex items-center']/li"))
#     subpageURL = []
#     browser = scrollDown(driver, 10)
#     time.sleep(10)
#     for i in range(numLinks - 1):
#           driver.get('https://labelleboucle.fr/collections/' + ticker + '?page=' + str(i +1))
#           element = driver.find_elements(By.CLASS_NAME, "card-product")
#           browser = scrollDown(driver, 5)
#           time.sleep(10)
#           browser = scrollDown(driver, 10)
#           time.sleep(10)
#           for a in element:
#                 subURL = a.find_element(By.TAG_NAME, 'a').get_attribute('href')
#                 subpageURL.append(subURL)

#     # transform into a data frame
#     dic = {'Label': ticker, 'URL': subpageURL}
#     df = df.append(pd.DataFrame(dic), ignore_index = True)


# print(df)
# df.to_csv('datasets/url_cosmetic.csv', encoding = 'utf-8-sig', index = False)
 

df = pd.read_csv('datasets/url_cosmetic.csv')
# add columns
df2 = pd.DataFrame(columns=['brand', 'name', 'price', 'ingredients'])
df = pd.concat([df, df2], axis = 1)

for i in range(len(df)+1):
    url = df.URL[i]
    driver.get(url)
    time.sleep(5)

    df.brand[i] = driver.find_element(By.CSS_SELECTOR, '.hidden.mb-2.text-sm.md\:block.uppercase').text
    df.name[i] = driver.find_element(By.CSS_SELECTOR, '.mb-2.text-xl.font-extrabold.md\:block').text

    try:
        df.price[i] = driver.find_element(By.XPATH, "//div[@id='price-template--14595359211590__main']/span[@class='text-2xl font-bold']").text
    except NoSuchElementException:
        df.price[i] = 'No Info'

    browser = scrollDown(driver, 1)
    time.sleep(5)
    browser = scrollDown(driver, 1)
    time.sleep(5)

    try:
        xpath = "//tabs-buttons[@class='justify-center gap-4 mb-8']/div[@class='block transition-all border-0 border-black cursor-pointer selected:border-b-2 selected:font-bold'][3]"
        btn = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", btn)
        xpath2="//tabs-panels/div[@class='block mt-4']/div[@class='text-sm']/div"
        df.ingredients[i] = driver.find_element(By.XPATH, xpath2).text
    except NoSuchElementException:
        df.ingredients[i] = 'No Info'
    df.to_csv('datasets/cosmetic.csv', encoding = 'utf-8-sig', index = False)
    print(i)

print(df)

df.to_csv('datasets/cosmetic.csv', encoding = 'utf-8-sig', index = False)

#driver.get('https://labelleboucle.fr/collections/laver')
#driver.find_element(By.XPATH, "//div[@class='flex justify-center']/nav/ul[@class='flex items-center']/li[5]/a[@class='block bg-sable w-5 h-5 p-5 rounded-lg scroll-ml-3']").click()

# element = driver.find_elements(By.CLASS_NAME, "card-product")
# subpageURL = []
# for a in element:
#         subURL = a.find_element(By.TAG_NAME, 'a').get_attribute('href')
#         subpageURL.append(subURL)
# print(subpageURL)


#print(numLinks)

#for i in range(numLinks - 1):