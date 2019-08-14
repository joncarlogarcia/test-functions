import pandas
from shapely.wkt import loads
from shapely.geometry import MultiLineString
import ast
import time

start_time = time.time()

fileOD = pandas.read_csv("OD_List.csv")

ix = fileOD.od_id

fileRP = pandas.read_csv("Trinoma_1_Routes_Pairs.csv")

pid = fileRP.point_id
lid = fileRP.list_id

fileRL = pandas.read_csv("Trinoma_1_Routes_List.csv")

identifier = fileRL.id
gm = fileRL.geom
tg = fileRL.tag

fileN = pandas.DataFrame()

fileN['line_id'] = 'NaN'
fileN['geom'] = 'NaN'

n = 0

for i, r in fileOD.iterrows():

    for index, row in fileOD.iterrows():

        if r['od_id'] == row['od_id']:

            pass

        else:

            line_coords = []
            coords_count = []
            idlist = []
            save_points = []
            by_product = []
            stop = 'NaN'
            rid = r['od_id']

            while stop != row['od_id']:

                d_list = []

                if row['od_id'] not in ast.literal_eval(lid[pid == rid].iloc[0]):

                    for h in ast.literal_eval(lid[pid == rid].iloc[0]):

                        if len(save_points) > 0 and rid not in save_points:

                            if tg[identifier == h].iloc[0] == "node" or h in idlist or len(set(loads(gm[identifier == h].iloc[0]).coords) & set(loads(gm[identifier == save_points[-1]].iloc[0]).coords)) > 0:

                                pass

                            else:

                                d_list.append([loads(gm[identifier == h].iloc[0]).centroid.distance(loads(gm[identifier == row['od_id']].iloc[0]).centroid), loads(gm[identifier == h].iloc[0]), h])

                        else:

                            if tg[identifier == h].iloc[0] == "node" or h in idlist:

                                pass

                            else:

                                d_list.append([loads(gm[identifier == h].iloc[0]).centroid.distance(loads(gm[identifier == row['od_id']].iloc[0]).centroid), loads(gm[identifier == h].iloc[0]), h])

                    if len(d_list) > 1 and rid not in save_points and tg[identifier == rid].iloc[0] != "node":

                        if len(save_points) > 0:

                            if save_points[-1] in ast.literal_eval(lid[pid == rid].iloc[0]):

                                pass

                            else:

                                save_points.append(rid)

                        else:

                            save_points.append(rid)

                    elif len(d_list) == 0 and rid in save_points:

                        save_points.remove(rid)

                    try:

                        if rid in save_points and len(line_coords) > 1:

                            if len(set(tuple(min(d_list)[1].coords)) & set(line_coords[-2]) & set(line_coords[-1])) > 0:

                                by_product.append(rid)

                            line_coords.append(tuple(min(d_list)[1].coords))
                            coords_count.extend(list(min(d_list)[1].coords))
                            rid = min(d_list)[2]
                            idlist.append(rid)

                            temp_l = list(min(d_list)[1].coords)

                            if coords_count.count(temp_l[0]) > 2 or coords_count.count(temp_l[1]) > 2:

                                rid = save_points[-1]
                                del line_coords[line_coords.index(tuple(loads(gm[identifier == rid].iloc[0]).coords)) + 1:]
                                del coords_count[(line_coords.index(tuple(loads(gm[identifier == rid].iloc[0]).coords)) + 1) * 2:]

                            else:

                                pass

                        else:

                            line_coords.append(tuple(min(d_list)[1].coords))
                            coords_count.extend(list(min(d_list)[1].coords))
                            rid = min(d_list)[2]
                            idlist.append(rid)

                            temp_l = list(min(d_list)[1].coords)

                            if coords_count.count(temp_l[0]) > 2 or coords_count.count(temp_l[1]) > 2:

                                rid = save_points[-1]
                                del line_coords[line_coords.index(tuple(loads(gm[identifier == rid].iloc[0]).coords)) + 1:]
                                del coords_count[(line_coords.index(tuple(loads(gm[identifier == rid].iloc[0]).coords)) + 1) * 2:]

                            else:

                                pass

                    except ValueError:

                        rid = save_points[-1]
                        del line_coords[line_coords.index(tuple(loads(gm[identifier == rid].iloc[0]).coords)) + 1:]
                        del coords_count[(line_coords.index(tuple(loads(gm[identifier == rid].iloc[0]).coords)) + 1) * 2:]

                else:

                    for b in by_product:

                        try:

                            g = tuple(loads(gm[identifier == b].iloc[0]).coords)
                            line_coords.remove(g)

                        except ValueError:

                            pass

                    line_coords.append(tuple(loads(gm[identifier == row['od_id']].iloc[0]).coords))
                    fileN.loc[n, 'geom'] = str(MultiLineString(line_coords))
                    fileN.loc[n, 'line_id'] = n
                    n += 1
                    stop = row['od_id']

fileN.to_csv("Generated.csv", index=False)

print(time.time() - start_time, "time")
