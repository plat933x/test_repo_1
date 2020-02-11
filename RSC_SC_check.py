from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# MOZILLA FIREFOX BROWSER
# driver = webdriver.Firefox(executable_path=r"C:\GEM\ALL\geckodriver.exe")
# driver = webdriver.Firefox()


# CHROME BROWSER, options first, 'driver=' second
from typing import Any

options = webdriver.ChromeOptions()
options.add_experimental_option('useAutomationExtension', False)
# headless argument does not open browser
#options.add_argument('headless')
driver = webdriver.Chrome(executable_path=r"C:\GEM\ALL\chromedriver.exe", options=options)


i = 0
while i < 3:
    print("Waiting for connection.", end='')
    i+=1
    for i in range(4):
        print('.', end='')
        time.sleep(1)

driver.get("http://172.16.250.248:8888/gem/rsc/soundcube")
driver.implicitly_wait(2)
login_button = driver.find_element_by_xpath('//button[@class="rLogin ui-btn ui-shadow ui-corner-all"]')
tytul = driver.title
#login_button = WebDriverWait(driver,8).until(EC.presence_of_element_located(By.XPATH, '//button[@class="rLogin ui-btn ui-shadow ui-corner-all"]'))
if login_button is None:
    print("GEM cannot be reached with browser.")
    quit()
login_button.click()
time.sleep(3)

driver.implicitly_wait(2)
#time.sleep(2)
#zmienna = driver.find_element_by_xpath("//label[@class='ui-input-text ui-body-inherit ui-corner-all ui-shadow-inset']/::/following_sibling::input[@name='text-1]")
zmienna = driver.find_element_by_xpath('//*[@action="wid=0&id=1"]')
signal_flow = zmienna.get_attribute("value")
print("\nSignal Flow ID: ", signal_flow)
time.sleep(1)
zmienna = driver.find_element_by_xpath('//input[@wid="13"]')
amp_type = zmienna.get_attribute("value")
print("Amplifier type: ", amp_type)
driver.quit()


