# This program represents the sizes of the continents on a pie chart

import sqlite3
import matplotlib.pyplot as plt
import numpy as np

continent = {}
connection = sqlite3.connect("country_data.sqlite")
cursor = connection.cursor()
cursor.execute('SELECT Country.name, Continent.name FROM Country INNER JOIN Continent ON '
               'Country.continentId=Continent.continentId;')

for row in cursor:
    if row[1] not in continent:
        continent[row[1]] = 1
    else:
        continent[row[1]] += 1

print(continent)
sizes = np.array([value for key, value in continent.items()])
labels = [key for key, value in continent.items()]

explode = (0, 0, 0, 0, 0, 0.3, 0.2)  # only "explode" the last two slices

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()
