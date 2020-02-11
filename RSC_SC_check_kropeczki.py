from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

import time
# MOZILLA FIREFOX BROWSER
# driver = webdriver.Firefox(executable_path=r"C:\GEM\ALL\geckodriver.exe")
# driver = webdriver.Firefox()


# CHROME BROWSER, options first, 'driver=' second

options = webdriver.ChromeOptions()
options.add_experimental_option('useAutomationExtension', False)
# headless argument does not open browser
options.add_argument('headless')
driver = webdriver.Chrome(executable_path=r"C:\GEM\ALL\chromedriver.exe", options=options)


print("Waiting for connection...", end='')
j = 0
while j<8:
    timer = 8
    login = driver.get("http://172.16.250.248:8888/gem/rsc/soundcube")
    print('.', end='')
    j += 1
    time.sleep(1)


    driver.find_element_by_xpath('//*[@class="rLogin ui-btn ui-shadow ui-corner-all"]').click()
    driver.implicitly_wait(2)
    #time.sleep(2)
    zmienna = driver.find_element_by_xpath('//*[@action="wid=0&id=1"]')
    signal_flow = zmienna.get_attribute("value")
    print("\nSignal Flow ID: ", signal_flow)
    time.sleep(1)
    zmienna = driver.find_element_by_xpath('//input[@wid="13"]')
    amp_type = zmienna.get_attribute("value")
    print("Amplifier type: ", amp_type)
    #login = WebDriverWait(driver, timer)

if j>7:
    print("\nConnection cannot be established")
    driver.quit()


    #driver.implicitly_wait(3)
    #driver.find_element_by_xpath('//*[@class="rLogin ui-btn ui-shadow ui-corner-all"]').click()
    #time.sleep(2)

    #zmienna = driver.find_element_by_xpath('//*[@action="wid=0&id=1"]')
    #signal_flow = zmienna.get_attribute("value")
    #print("Signal Flow ID: ", signal_flow)

    #zmienna = driver.find_element_by_xpath('//input[@wid="13"]')
    #amp_type = zmienna.get_attribute("value")
    #print("Amplifier type: ", amp_type)
    #driver.quit()



    print('*' * 150)
    print("GEM is unreachable - connection cannot be established.")

