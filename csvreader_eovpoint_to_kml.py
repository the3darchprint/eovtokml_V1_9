import csv
# import requests
import simplekml
import easygui
from pyproj import Transformer
transformer_from_EOV = Transformer.from_crs("epsg:23700", "epsg:4326")
transformer_from_KML = Transformer.from_crs("epsg:4326", "epsg:23700")


def fromcsvtokml():

    kml=simplekml.Kml()

    file = easygui.fileopenbox(filetypes=["*.csv"])
    fileoutput = easygui.filesavebox(default="csv_export.kml", filetypes=["*.kml"])

    f = open(file, mode="r")
    reader = csv.reader(f, delimiter=";")

    coords_from_csv = []

    for row in reader:
        # koords.append(row)
        coords_from_csv.append([str(row[0]), float(row[1]), float(row[2])])

    wgscoords_from_coords = []

    for i in coords_from_csv:
        pointname = i[0].replace("ď»ż", "")
        ycoord = i[1]
        xcoord = i[2]

        coords=transformer_from_EOV.transform(ycoord, xcoord)

        # http = str(f"http://www.agt.bme.hu/on_line/etrs2eov/etrs2eov.php?e={ycoord}&n={xcoord}&sfradio=single&format=TXT")
        # coords = requests.get(http)
        # coordstext = str(coords.text)
        # wgslist = coordstext.split()
        wgs84y = coords[0]
        wgs84x = coords[1]
        wgscoords_from_coords.append([pointname, wgs84y, wgs84x])

    for row in wgscoords_from_coords:
        kml.newpoint(name=row[0], coords=[(row[2], row[1])])

    kml.save(fileoutput)





