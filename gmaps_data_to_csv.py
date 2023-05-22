# import libraries
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options 

from prettytable import PrettyTable
from time import sleep
import pandas as pd

# set options
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')

# open the browser / webdriver
driver = webdriver.Firefox(service=Service(r"~/.wdm/drivers/geckodriver"), options=options)

# load the webpage
driver.get("https://www.google.com/maps/")

# get input element and send key to search
input_search = driver.find_element(By.XPATH, '//input[@id="searchboxinput"]')
input_search.send_keys("universitas di jakarta")
input_search.send_keys(Keys.ENTER)

sleep(17)

# get container of search's result
container = driver.find_element(By.XPATH, '//div[@role="feed"]')
sleep(10)

elem_not_found = True
while elem_not_found:
    try:
        # scroll down
        container.send_keys(Keys.PAGE_DOWN)

        sleep(1)

        WebDriverWait(driver, 5).until( 
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[class="HlvSq"]'))
        )

        elem_not_found = False
    except:
        continue

results = []

result_list = container.find_elements(By.CSS_SELECTOR, 'div[role="article"]')

for element in result_list:

    # grab info
    title = element.find_element(By.CSS_SELECTOR, 'div[class="qBF1Pd fontHeadlineSmall "]').get_attribute('innerText')
    try:
        address = WebDriverWait(driver, 1).until(
            EC.visibility_of(
                # element.find_element(By.XPATH, '//div[@class="W4Efsd"]/span[2]/span[2]')
                element.find_element(By.CSS_SELECTOR, 'div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > span:nth-child(2) > span:nth-child(2)')
            )
        ).get_attribute('innerText')
    except:
        address = '-'

    try:
        phone = WebDriverWait(driver, 1).until(
            EC.visibility_of(
                element.find_element(By.XPATH, '//div[@class="W4Efsd"][2]/span[2]/span[2]')
                # element.find_element(By.CSS_SELECTOR, 'div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > span:nth-child(1) > span:nth-child(1)')
            )
        ).get_attribute('innerText')
    except:
        phone = '-'
    
    try:
        rating = WebDriverWait(driver, 1).until(
            EC.visibility_of(
                element.find_element(By.CSS_SELECTOR,'span[class="ZkP5Je"]')
            )
        ).get_attribute('aria-label').strip().split(' ')
        star_rating = rating[1]
        num_reviews = rating[2] 
        # print(rating)
    except:
        star_rating = '-'
        num_reviews = '-'

    results.append([title, address, phone, star_rating, num_reviews])


# print to screen
columns = ["InstitutionName", "Address", "Phone", "Star Rating", "NumberOfReviews"]
table = PrettyTable(
    field_names = columns
)

table.add_rows(results)
print(table)
print(len(result_list))

# save to csv
df = pd.DataFrame(results, columns=columns)
df.to_csv('extract_data_from_gmaps.csv')