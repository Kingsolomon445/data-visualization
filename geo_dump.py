# This is used to write the records into the geo_location.js file , saving the longitude and latitude of the countries.

import sqlite3
import json
import codecs

conn = sqlite3.connect('country_data.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM Locations')
fhand = codecs.open('geo_location.js', 'w', "utf-8")
fhand.write("myData = [\n")
count = 0
for row in cur:
    data = str(row[2].decode())
    try:
        js = json.loads(str(data))
    except:
        continue

    if not ('status' in js and js['status'] == 'OK'):
        continue

    lat = js["results"][0]["geometry"]["location"]["lat"]
    lng = js["results"][0]["geometry"]["location"]["lng"]
    if lat == 0 or lng == 0:
        continue
    where = js['results'][0]['formatted_address']
    where = where.replace("'", "")
    try:
        print(where, lat, lng)

        count = count + 1
        if count > 1:
            fhand.write(",\n")
        output = "[" + str(lat) + "," + str(lng) + ", '" + where + "']"
        fhand.write(output)
    except:
        continue

fhand.write("\n];\n")
cur.close()
fhand.close()
print(count, "records written to geo_location.js")
print("Open geo_data.html to view the data in a browser")
