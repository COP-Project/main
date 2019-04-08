from readPlate import readaPlate, create_alpr, destroy_alpr

myalpr = create_alpr()

def test_OALPR(myalpr, state, img):
    plates = readaPlate(myalpr, state, img)
    return plates[0]


assert readaPlate(myalpr, 'mt', '../img/mt.jpg')[0] == 'BJR216'
assert readaPlate(myalpr, 'ca', '../img/ca.jpeg')[0] == '7VDV740'
