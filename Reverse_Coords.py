from shapely.wkt import loads
from shapely.geometry import Polygon
import re
import csv

csv.field_size_limit(1000000)

file = open("Routes_Buffered3.csv")
read = csv.DictReader(file)

file2 = open("Routes_Buffered4.csv", 'w')
names = ['id', 'name', 'category', 'line_points']
write = csv.DictWriter(file2, lineterminator='\n', fieldnames=names)
write.writeheader()

for i in read:

    cut = re.split(r'[()]', i['line_points'])
    cut2 = re.split(r'[,]', cut[2])
    cut4 = re.split(r'[,]', cut[2])
    nodes2 = []
    nodes4 = []

    if cut2 == [''] or len(cut2) < 3:
        pass

    elif cut4 == [''] or len(cut2) < 3:
        pass

    else:

        for coords in cut2:

            cut3 = re.split(r'[ ]', coords)
            retype = float(cut3[1]), float(cut3[0])
            nodes2.append(tuple(retype))

        for coords in cut4:
            cut3 = re.split(r'[ ]', coords)
            retype = float(cut3[1]), float(cut3[0])
            nodes4.append(tuple(retype))

        write.writerow({'id': i['id'], 'name': i['name'], 'category': i['category'], 'line_points': Polygon(tuple(nodes2), tuple(nodes4))})
        del nodes2[:]
        del nodes4[:]
