import sys
import time
import csv
from selenium import webdriver


with open('tnrref.csv', 'rt', encoding='utf8') as csvfile:
    langs = csv.reader(csvfile, delimiter=',', quotechar='"')
    for i in range(10):
        print(" ")

users = [3,4,"kupa"]
print(users[0])

