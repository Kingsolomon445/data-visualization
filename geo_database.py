# This is used to create and set up the database


import json
import sqlite3
import ssl
import time
import urllib.parse
import urllib.request

api_key = 42
serviceurl = "http://py4e-data.dr-chuck.net/json?"

with open("country_data.json", "r") as fname1:
    country = fname1.read()
with open("continent_data.json", "r") as fname2:
    continent = fname2.read()

connection = sqlite3.connect('country_data.sqlite')
cursor = connection.cursor()
cursor.executescript('''

CREATE TABLE IF NOT EXISTS Continent (
    continentId     VARCHAR(20) NOT NULL,
    name            TEXT,
    PRIMARY KEY (continentId)
);

CREATE TABLE IF NOT EXISTS Country (
    countryId     VARCHAR(20) NOT NULL,
    name          TEXT,
    capital       VARCHAR(100),
    currency      VARCHAR(20),
    continentId   VARCHAR(20),
    PRIMARY KEY(countryId),
    FOREIGN KEY(continentId) REFERENCES Continent(continentId)
);

CREATE TABLE IF NOT EXISTS Locations (
    countryId VARCHAR(20),
    country TEXT,
    geodata TEXT,
    FOREIGN KEY(countryId) REFERENCES Country(countryId)
)

''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

country = json.loads(country)
continent = json.loads(continent)
continent_columns = ["objectId", "name"]
country_columns = ["objectId", "name", "capital", "currency", "continent"]
for row in continent["results"]:
    keys = tuple(row[c] for c in continent_columns)
    cursor.execute('INSERT OR IGNORE INTO Continent VALUES(?, ?)', keys)
    print(f'{row["name"]}, {row["objectId"]} data inserted Successfully')

print("\n\n")
for row in country["results"]:
    keys = tuple(row[c] if c != "continent" else row[c]["objectId"] for c in country_columns)
    cursor.execute('INSERT OR IGNORE INTO Country VALUES(?, ?,?,?,?)', keys)
    print(f"{row['name']}, {row['objectId']} data inserted successfully")

count = 0
for row in country["results"]:
    address = row["name"].strip()
    country_id = row["objectId"]
    if count > 100:
        print('Retrieved 100 locations, restart to retrieve more')
        break

    print('')
    cursor.execute("SELECT geodata FROM Locations WHERE country= ?",
                   (memoryview(address.encode()),))

    try:
        data = cursor.fetchone()[0]
        print("Found in database ", address)
        continue
    except:
        pass

    parms = dict()
    parms["address"] = address
    url = serviceurl + urllib.parse.urlencode(parms)

    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))
    count += 1

    try:
        js = json.loads(data)
    except:
        print(data)  # We print in case unicode causes an error
        continue

    if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS'):
        print('==== Failure To Retrieve ====')
        print(data)
        break

    cursor.execute('''INSERT OR IGNORE INTO Locations (countryId, country, geodata)
            VALUES (?, ?, ? )''', (country_id, memoryview(address.encode()), memoryview(data.encode())))
    if count % 10 == 0:
        print('Pausing for a bit...')
        time.sleep(1)

print("Run geodump.py to read the data from the database so you can vizualize it on a map.")

connection.commit()
connection.close()
