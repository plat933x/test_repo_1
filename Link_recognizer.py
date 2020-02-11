from selenium import webdriver
import Record
import threading
import timeit
import config
import re, os
import time
import Audio_compar
import Audio_cuting

from selenium.common.exceptions import NoSuchElementException


def linkdetection():
    config.link_test=True
    counter = 0
    options = webdriver.ChromeOptions()
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    driver.get("http://172.16.250.248:8080")
    time.sleep(0.5)
    while counter != 100:
        try:
            driver.find_element_by_xpath('//*[@id="native-radio"]').click()
            counter += 1
            time.sleep(0.1)
            break
        except:
            continue
    if counter == 100:
        config.server_adress.send(
            bytes(str('Get_screenshoot: something went wrong with snapshot') + '\r\n', encoding='utf-8'))
        config.server_adress.send(bytes(str('stop: -2') + '\r\n', encoding='utf-8'))
        config.server_adress.close()
        config.driver.quit()
        return -2
    counter = 0
    while counter != 100:
        try:
            driver.find_element_by_xpath(
                '//*[@id="Screen:TUNER_PLAYER_*"]/div/au3-station-list/au3-list/div[1]/div/div[1]/div[2]/div[4]/div[1]/au3-radio-station-list-item/div').click()
            counter += 1
            time.sleep(0.1)
            break
        except:
            continue
    if counter == 100:
        config.server_adress.send(
            bytes(str('Get_screenshoot: something went wrong with snapshot') + '\r\n', encoding='utf-8'))
        config.server_adress.send(bytes(str('stop: -3') + '\r\n', encoding='utf-8'))
        config.server_adress.close()
        config.driver.quit()
        return -3
    while counter <= 2000:
        if counter == 2000:
            print("Counter to small, Longer time to tune is needed")
            return -2
        try:
            station_type = driver.find_element_by_xpath('//*[@id="Screen:TUNER_PLAYER_*"]/div/au3-nps/div/div/div/au3-radio-nps-metadata/div/div[1]/au3-icon/img')
            station_name = driver.find_element_by_xpath('//*[@id="StationName"]/span')
            station_name = station_name.get_attribute("innerHTML")
        except NoSuchElementException:
            counter += 1
            continue
        else:
            break
    current = re.findall("(radio_)(\w+)", station_type.get_attribute("src"))
    station_type=current[0][1]
    t1 = threading.Thread(target=Record.Record, args=('record_on_demand','C:/YA_MIB3/logs/audio/link_audio', 20 ))
    t1.start()
    while 1:
        if re.findall("(radio_)(\w+)",driver.find_element_by_xpath('//*[@id="Screen:TUNER_PLAYER_*"]/div/au3-nps/div/div/div/au3-radio-nps-metadata/div/div[1]/au3-icon/img').get_attribute("src"))[0][1] != station_type:
            stop=timeit.default_timer()
            config.stop_request=1
            break
        elif driver.find_element_by_xpath('//*[@id="StationName"]/span').get_attribute("innerHTML") != station_name:
            stop = timeit.default_timer()
            config.stop_request = 1
            break
    t1.join()
    cut_time=int((stop-config.start_time)*1000)
    Path = (Audio_cuting.Audio_cuting(cut_time+200, config._recordondemand_path_, 5000))# 200 is delay of audio change compare to indicator change on HMI eth
    os.remove(config._recordondemand_path_)
    Audio_compar.Audio_analyzer([0, Path[0], Path[1]])
if __name__ == "__main__":
    linkdetection()