from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

query = input('검색할 키워드를 입력하세요: ')
print('--------------------------------')

url = 'https://www.naver.com/'
driver = webdriver.Chrome()
driver.get(url)
time.sleep(2)

search_box = driver.find_element(By.ID, 'query')
search_box.send_keys(query)
search_box.send_keys(Keys.RETURN)
time.sleep(2)

driver.find_element(By.XPATH, '//*[@id="lnb"]/div[1]/div/div[1]/div/div[1]/div[1]/a').click()
time.sleep(3)

news_titles = driver.find_elements(By.CLASS_NAME, 'sds-comps-text-type-headline1')
for i in news_titles:
    title = i.text
    print(title)




