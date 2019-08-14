import pymysql
from shapely.geometry import Point, MultiLineString, LineString, Polygon
from shapely.wkt import loads
from osgeo import ogr
import re
import csv


def create(vehicle_id, start_date, end_date):

    csv.field_size_limit(1000000000)

    connection = pymysql.connect(host='000.000.000.00',
                                 user='user',
                                 password='pass',
                                 db='database',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.SSDictCursor)

    cur = connection.cursor()

    # execute a select query and return results as a generator

    def generator(stmt):
        # error handling code removed
        cur.execute(stmt)

        for row in cur:
            yield row

    sql = "select latitude, longitude from ngp.hist_trackrecords where device_id='%s'  and reportstamp between '%s' and '%s'" % (vehicle_id, start_date, end_date)

    pts = set()

    for l in generator(sql):
        pts.add(str(Point(l['longitude'], l['latitude'])))

    connection.close()

    point_list = list(pts)

    road = open('roads.csv')
    read = csv.reader(road)

    for j in read:
        m = loads(j[0])

    line_list = []

    c = 0

    for r in point_list:
        if c != (len(point_list) - 1):
            line = LineString([m.interpolate(m.project(loads(r))),
                               m.interpolate(m.project(loads(point_list[c + 1])))])
            line_list.append(line)
            c += 1

    ml = MultiLineString(line_list)
    geom = ogr.CreateGeometryFromWkt(str(ml))
    length = int(geom.Length())

    bml_in = str(ml.buffer(.0001))

    cut = re.split(r'[()]', bml_in)
    cut2 = re.split(r'[,]', cut[2])
    nodes = []

    if cut2 == [''] or len(cut2) < 3:
        pass

    else:
        for coords in cut2:
            cut3 = re.split(r'[ ]', coords)
            retype = float(cut3[1]), float(cut3[0])
            nodes.append(tuple(retype))

    bml_out = Polygon(nodes)

    return bml_out, length
