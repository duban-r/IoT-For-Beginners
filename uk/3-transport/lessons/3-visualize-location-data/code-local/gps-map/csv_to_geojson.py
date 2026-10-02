import csv
import json

features = []

with open('gps_data.csv', newline='') as file:
    for row in csv.DictReader(file):
        features.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [float(row['lon']), float(row['lat'])]
            },
            'properties': {
                'timestamp': row['timestamp']
            }
        })

geojson = {
    'type': 'FeatureCollection',
    'features': features
}

with open('gps_data.js', 'w') as file:
    file.write('const gpsData = ' + json.dumps(geojson, indent=2) + ';\n')

print('Записано точок:', len(features))
