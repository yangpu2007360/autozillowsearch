from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
accept_language = "en-US,en;q=0.9"

header = {
    "User-Agent": user_agent,
    "Accept-Language": accept_language
}

zillow_url = "https://www.zillow.com/castro-valley-ca/?searchQueryState=%7B%22usersSearchTerm%22%3A%22Castro%20Valley%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.1426742258252%2C%22east%22%3A-121.98663403417481%2C%22south%22%3A37.668108690974265%2C%22north%22%3A37.75705732006734%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A30785%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22price%22%3A%7B%22max%22%3A2500000%2C%22min%22%3A800000%7D%2C%22mp%22%3A%7B%22max%22%3A8400%2C%22min%22%3A2688%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%2C%22category%22%3A%22cat1%22%2C%22pagination%22%3A%7B%7D%7D"
response = requests.get(zillow_url, headers=header)

soup = BeautifulSoup(response.text, "html.parser")

houses_info = soup.findAll(name="address", class_="list-card-addr")
address_list = []

for house in houses_info:
    address_list.append(house.getText())
print(address_list)
print(len(address_list))

price_info = soup.findAll(class_="list-card-price")
price_list = []

for price in price_info:
    price_list.append(int(price.getText().replace("$", "").replace(",", "")))

print(price_list)
print(len(price_list))
link_list = []
link_info = soup.findAll(class_="list-card-link", href=True)
for num in range(0, len(link_info), 2):
    link_list.append(link_info[num]['href'])

print(link_list)
print(len(link_list))

survey_url = "https://docs.google.com/forms/d/e/1FAIpQLSclPfpvS4FG0ykAtQpQM44hfnMDD4Us38qAE65FxOZSEq3RfQ/viewform"
s = Service('/Users/puyang/chromedriver')
driver = webdriver.Chrome(service=s)

time.sleep(5)


def submit_info(num):
    driver.get(survey_url)
    address_enter = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_enter.send_keys(address_list[num])
    time.sleep(2)
    price_enter = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_enter.send_keys(price_list[num])
    time.sleep(2)
    link_enter = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_enter.send_keys(link_list[num])
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span').click()


for num in range(0, len(address_list)):
    print(num)
    try:
        submit_info(num)
    except ElementNotInteractableException:
        pass
