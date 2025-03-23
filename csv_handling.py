import csv
import itertools

with open("csv_data.csv", newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    for index, element in enumerate(itertools.islice(reader, 8)):
        print(f"{index}: {element}")
    print()

    eight_row = next(reader)
    eight_element = eight_row[0]
    print(f"Next row out of for loop: {eight_element}")