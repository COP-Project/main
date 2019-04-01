from readPlate import readaPlate, create_alpr, destroy_alpr
from openalpr import Alpr

myalpr = create_alpr('us')
x = readaPlate(myalpr, 'ca', 'ferrari.jpg')
destroy_alpr(myalpr)
print(len(x))
for plate in x:
    print('Plate: ' + plate)
