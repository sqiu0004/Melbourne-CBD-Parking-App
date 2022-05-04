import geojson
import urllib
from geojson import Point, Feature, FeatureCollection, dump
import csv
from collections import defaultdict
with open('weekly_table_2018-20_MarkerId.csv', newline="") as csvfile, open('On-street Parking Bays(1).geojson') as f:
    columns = defaultdict(list)
    reader = csv.DictReader(csvfile)
    gj = geojson.load(f)
    features = gj["features"]
    goodData = {"type": "FeatureCollection", "features": []}
    j=0
    for row in reader:
        for (k, v) in row.items():  # go over each column name and value
            columns[k].append(v)
    for x in features:
        table = []
        Sum = 0
        for y in columns[x["properties"]["marker_id"]]:
            Sum += float(y)
        x["properties"].pop("rd_seg_id")
        x["properties"].pop("meter_id")
        x["properties"].pop("rd_seg_dsc")
        x["properties"].pop("last_edit")
        if Sum != 0:
            for i in columns[x["properties"]["marker_id"]]:
                table.append(int(float(i)))
            x["properties"]["prob"] = table
            goodData["features"].append(x)
            j=j+1
with open("weekly2018markerID.geojson", 'w') as d:
    dump(goodData, d)
