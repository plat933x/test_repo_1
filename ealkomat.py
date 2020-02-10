from selenium import webdriver
from selenium.webdriver.support.select import Select
import time

def ja_ealkomat(ile_waze=90, ile_wzrostu=150, ile_piw=3, ile_wodki=350, start_picia="21", ile_trwalo_picie="4"):
    driver = webdriver.Firefox(executable_path=r"D:\Users\Master\PycharmProjects\untitled\geckodriver.exe")
    driver.implicitly_wait(3)
    driver.maximize_window()
    driver.get("https://www.ilemogewypic.pl/alkomat.php")
    print(driver.title)
    # time.sleep(2)
    driver.execute_script("window.scrollTo(0, 700)")

    kobieta = driver.find_element_by_css_selector("input[type='radio'][value='k']")
    mezczyzna = driver.find_element_by_css_selector("input[type='radio'][value='m']")
    mezczyzna.click()

    waga = driver.find_element_by_id("waga")
    waga.send_keys(ile_waze)
    time.sleep(0.5)
    wzrost = driver.find_element_by_id("wzrost")
    wzrost.send_keys(ile_wzrostu)
    time.sleep(0.5)
    wodka = driver.find_element_by_id("ilosc1")
    wodka.send_keys(ile_wodki)
    time.sleep(0.5)
    piwa = driver.find_element_by_id("ilosc3")
    piwa.send_keys(ile_piw)
    time.sleep(0.5)

    godziny_picia = driver.find_element_by_id("godzina")
    sel = Select(godziny_picia)
    sel.select_by_value(start_picia)

    czas_picia = driver.find_element_by_id("czaspicia")
    sel = Select(czas_picia)
    sel.select_by_value(ile_trwalo_picie)

    oblicz = driver.find_element_by_class_name("przyciskOblicz")
    oblicz.click()
    print("Obliczanie zawartosci alkoholu...")

    #zawartosc = ( )
    #print(type(zawartosc))
    promile = []
    promile = driver.find_elements_by_xpath('//span[@class="tab"]')
    print(type(promile))

    for i promile:

    driver.quit()

    #print(promil_max)




# print("Max wartosc promili wyniosła " + max_promil)

ja_ealkomat()
