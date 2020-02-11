from selenium import webdriver
from selenium.common.exceptions import *
import time
import config
from datetime import datetime
import ctypes
def start_web_driver():
    user32 = ctypes.windll.user32
    x,y = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
    try:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('headless')
        config.driver = webdriver.Chrome(executable_path=r'C:\AudioAnalyzer\chromedriver.exe',options=options, service_args=["hide_console"])
        config.driver.set_window_size(x/2, y+y/2)
    except WebDriverException as exception:
         config.webdriver = "chrome problem"
         return "chrome problem"
    try:
        config.driver.get("http://172.16.250.248:8080/#/main")
    except WebDriverException:
        config.driver.quit()
        config.webdriver = "web_side problem"
        return "web_side problem"
    # config.webdriver = ''
    return 0
def Get_screenshoot(path):
    counter = 0
    while counter != 20:
        try:
            counter += 1
            time.sleep(0.1)
            config.driver.find_element_by_xpath('// *[ @ id = "native-media"]').click()
            break
        except:
            continue
    if counter == 20:
        config.server_adress.send(bytes(str('Get_screenshoot: something went wrong with snapshot -1') + '\r\n', encoding='utf-8'))
        config.server_adress.send(bytes(str('stop: -1') + '\r\n', encoding='utf-8'))
        config.server_adress.close()
        config.driver.quit()
        return -1
    counter = 0
    time.sleep(0.5)
    while counter != 20:
        try:
            counter += 1
            time.sleep(0.1)
            config.driver.find_element_by_xpath('//*[@id="native-radio"]').click()
            break
        except:
            continue
    if counter == 20:
        config.server_adress.send(bytes(str('Get_screenshoot: something went wrong with snapshot -2') + '\r\n', encoding='utf-8'))
        config.server_adress.send(bytes(str('stop: -2') + '\r\n', encoding='utf-8'))
        config.server_adress.close()
        config.driver.quit()
        return -2
    counter = 0
    while counter != 40:
        try:
            counter += 1
            time.sleep(0.1)
            config.driver.find_element_by_xpath('//*[@id="Screen:TUNER_PLAYER_*"]/div/au3-station-list/au3-list/div[1]/div/div[1]/div[2]/div[4]/div[1]/au3-radio-station-list-item/div')
            break
        except:
            continue
    if counter == 40:
        config.server_adress.send(bytes(str('Get_screenshoot: something went wrong with snapshot -3') + '\r\n', encoding='utf-8'))
        config.server_adress.send(bytes(str('stop: -3') + '\r\n', encoding='utf-8'))
        config.server_adress.close()
        config.driver.quit()
        return -3
    time.sleep(1)
    filename = '{}/{:%Y-%m-%d_%H-%M-%S}.png'.format(path, datetime.today())
    config.server_adress.send(bytes(str('Get_screenshoot: Station list reached') + '\r\n', encoding='utf-8'))
    time.sleep(0.5)
    config.driver.save_screenshot(filename)
    counter = 0
    while counter != 20:
        try:
            counter += 1
            time.sleep(0.1)
            config.driver.find_element_by_xpath(
                '//*[@id="Screen:TUNER_PLAYER_*"]/div/au3-station-list/au3-list/div[1]/div/div[1]/div[2]/div[4]/div[1]/au3-radio-station-list-item/div').click()
            break
        except:
            continue
    if counter == 20:
        config.server_adress.send(bytes(str('stop: -4') + '\r\n', encoding='utf-8'))
        config.server_adress.close()
        config.driver.quit()
        return -4
    time.sleep(0.5)
    filename = '{}/{:%Y-%m-%d_%H-%M-%S}.png'.format(path, datetime.today())
    config.driver.save_screenshot(filename)
    config.server_adress.send(bytes(str('stop: '+ config._recordondemand_path_) + '\r\n', encoding='utf-8'))
    config.server_adress.close()
    config.driver.quit()
    return 0
