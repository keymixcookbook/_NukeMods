import csv

color_code = {}

with open("/Users/Tianlun/Documents/GitHub/_NukeStudio/__Misc/NukeColorCode.csv", 'r') as f:

    lines = csv.reader(f)

    for row in lines:
        color_code[row[0]] = [row[1], row[2], row[3]]

print color_code
