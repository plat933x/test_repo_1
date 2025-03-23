from selenium import webdriver
import time
# MOZILLA FIREFOX BROWSER
# driver = webdriver.Firefox(executable_path=r"geckodriver.exe")
# driver = webdriver.Firefox()

options = webdriver.ChromeOptions()
options.add_experimental_option('useAutomationExtension', False)
# headless argument does not open browser
#options.add_argument('headless')
driver = webdriver.Chrome(options=options)

i = 0
while i < 3:
    print("Waiting for connection.", end='')
    i+=1
    for i in range(4):
        print('.', end='')
        time.sleep(1)

driver.get("http://172.16.250.248:8888")
driver.implicitly_wait(2)
login_button = driver.find_element_by_xpath('//button[@class="rLogin ui-btn ui-shadow ui-corner-all"]')
tytul = driver.title

if login_button is None:
    print("Object cannot be reached with browser.")
    quit()
login_button.click()
time.sleep(3)

driver.implicitly_wait(2)

zmienna = driver.find_element_by_xpath('//*[@action="wid=0&id=1"]')
signal = zmienna.get_attribute("value")
print("\nSignal ID: ", signal)

time.sleep(2.5)

zmienna = driver.find_element_by_xpath('//input[@wid="13"]')
amp_type = zmienna.get_attribute("value")
print("Amplifier type: ", amp_type)
driver.quit()