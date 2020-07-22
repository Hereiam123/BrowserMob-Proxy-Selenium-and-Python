from browsermobproxy import Server
import psutil
import time
import json

for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() == "browsermob-proxy":
        proc.kill()

dict = {'port': 8090}
server = Server(path="", options=dict)
server.start()
time.sleep(1)
proxy = server.create_proxy()
time.sleep(1)

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

profile = webdriver.FirefoxProfile()
selenium_proxy = proxy.selenium_proxy()
profile.set_proxy(selenium_proxy)
options = FirefoxOptions()
options.headless = False
driver = webdriver.Firefox(firefox_profile=profile, options=options)
proxy.new_har("universal.com",options={'captureHeaders': True})
driver.get("https://www.universalorlando.com/web/en/us")

#fastrack = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, "/html/body/app-component/header/div/div[2]/div[2]/button[2]")))
#fastrack.click()

fastrack2 = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, "/html/body/app-component/upr-k2-layout/div/main/app-tcm-page/div/app-swim-lane[2]/section/upr-carousel/section[1]/div/div/section[1]/app-image-card/div/tcm-anchor/a")))
fastrack2.click()

time.sleep(10)

fastrack3 = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="btn-1"]')))
fastrack3.click()

time.sleep(10)

print (proxy.har) # returns a HAR JSON blob

result = json.dumps(proxy.har, ensure_ascii=False, indent=2, sort_keys=True)
print(result, file=open("output2.txt", "w"))

server.stop()
driver.quit()