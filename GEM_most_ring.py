from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

options = webdriver.ChromeOptions()
options.add_experimental_option('useAutomationExtension', False)
# headless argument does not open browser
#options.add_argument('headless')
driver = webdriver.Chrome(executable_path=r"C:\GEM\ALL\chromedriver.exe", options=options)

driver.get("http://172.16.250.248:8888/gem/coding")
driver.maximize_window()
driver.implicitly_wait(2)
login_button = driver.find_element_by_xpath('//button[@class="rLogin ui-btn ui-shadow ui-corner-all"]')
if login_button is not None:
    login_button.click()
    time.sleep(3)
else:
    print("No login page visible, proc finished")
    driver.close()

driver.execute_script("window.scrollTo(0, 1420);")
zmienna = driver.find_element_by_xpath("//label[@class='ui-input-text ui-body-inherit ui-corner-all ui-shadow-inset']/::/following_sibling::input[@name='text-1]")
#wybor = driver.find_element_by_xpath('//div[@action="wid=0&id=20"]//div[@index="1]').click()
print(zmienna.text)
#select = Select(driver.find_element_by_xpath('//*[@id="select-native-1-button"]'))


print("Scrolled down")
))