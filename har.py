from selenium import webdriver
from browsermobproxy import Server
import os
import json
from urllib.parse import urlparse
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pprint

server = Server(
    "")
server.start()
proxy = server.create_proxy(params={"trustAllServers":"true"})

chromedriver = ""
#os.environ["webdriver.chrome.driver"] = chromedriver
url = urlparse(proxy.proxy).path
#chrome_options = webdriver.ChromeOptions()
chrome_options = webdriver.FirefoxOptions()
chrome_options.add_argument('ignore-certificate-errors')
chrome_options.add_argument("--proxy-server={0}".format(url))
#driver = webdriver.Chrome(chromedriver, chrome_options=chrome_options)
driver = webdriver.Firefox(chromedriver, chrome_options)

proxy.new_har("universalorlando.com",
              options={'captureHeaders': True})
              
driver.get("https://www.universalorlando.com/")

#fastrack2 = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="btn-1"]')))
#fastrack2.click()

#time.sleep(3)

#Print to screen
#pprint.pprint(proxy.har)

#Dump to file
result = json.dumps(proxy.har, ensure_ascii=False, indent=2, sort_keys=True)
print(result, file=open("output.txt", "w"))
proxy.close()
driver.quit()
