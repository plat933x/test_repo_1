dict = {'apple': 1,'pear': 2,'plum': 3,'peach': 4}



with open('test.txt', 'w') as plik:
    if 'pear' in dict:
        for fruit in dict:
            plik.write(fruit+'\n')
    else:
        print('No fruit named pear in dictionary')

plik.close()
print('*'*90)

with open('test.txt', 'r') as pliczek:
        print(pliczek.read())

