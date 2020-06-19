import csv
import pandas as pd
import numpy as np


def load_cities_coordinates(file):
    localities = {}
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            localities[row['cidade']] = {'lat': float(row['lat']), 'lon': float(row['lon'])}
    return localities

def load_cities_dataframe(file):
    return pd.read_csv(file, sep=',', dtype={"fips": str})

def load_localities_coord_list(cities, localities_coord):
    data = []
    for city in cities:
        if city != 'nenhum':
            data.append([localities_coord[city]['lat'], localities_coord[city]['lon']])
    return data


def load_localities_coord_size_list(cities:pd.Series, localities_coord):
    data = []
    for (city,size) in cities.iteritems():
        if city != 'nenhum':
            data.append([localities_coord[city]['lat'], localities_coord[city]['lon'], size, city])
    return pd.DataFrame(data, columns=['lat', 'lon', 'size', 'city'])