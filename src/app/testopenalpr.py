from readPlate import readaPlate, create_alpr, destroy_alpr
from openalpr import Alpr
    
myalpr = create_alpr('sg')
x = readaPlate(myalpr, 'sg', '../img/SINGAsg.jpg')
print(str(len(x)) + ' plate(s) found')
for plate in x:
    print('Plate: ' + plate)


if myalpr.is_loaded:
    myalpr.set_country('us')

x = readaPlate(myalpr, 'mt', '../img/mt.jpg')
destroy_alpr(myalpr)
print(str(len(x)) + ' plate(s) found')
for plate in x:
    print('Plate: ' + plate)
