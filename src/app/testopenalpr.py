from readPlate import readaPlate, create_alpr, destroy_alpr
from openalpr import Alpr
    
myalpr = create_alpr('us')
x = readaPlate(myalpr, 'sg', 'sg', '../img/SINGAsg.jpg')
print(str(len(x)) + ' plate(s) found')
for plate in x:
    print('Plate: ' + plate)
    

x = readaPlate(myalpr, 'us', 'mt', '../img/mt.jpg')
destroy_alpr(myalpr)
print(str(len(x)) + ' plate(s) found')
for plate in x:
    print('Plate: ' + plate)
