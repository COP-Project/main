from readPlate import readaPlate, create_alpr, destroy_alpr
from openalpr import Alpr
    
myalpr = create_alpr()
x = readaPlate(myalpr, 'ca', '../img/ca.jpeg')
print(str(len(x)) + ' plate(s) found')
for plate in x:
    print('Plate: ' + plate)

x = readaPlate(myalpr, 'mt', '../img/mt.jpg')
print(str(len(x)) + ' plate(s) found')
for plate in x:
    print('Plate: ' + plate)
