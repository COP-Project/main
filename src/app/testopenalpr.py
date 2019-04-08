from readPlate import read_a_plate

assert read_a_plate('../img/mt.jpg', 'mt')[0] == 'BJR216'
print(read_a_plate('../img/mt.jpg', 'mt')[0])
assert read_a_plate('../img/ca.jpeg', 'ca')[0] == '7VDV740'
print(read_a_plate('../img/ca.jpeg', 'ca')[0])
