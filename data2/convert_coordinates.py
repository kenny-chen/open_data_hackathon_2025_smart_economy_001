import json
from pyproj import Transformer

# Transform from HK1980 Grid (EPSG:2326) to WGS84 (EPSG:4326)
transformer = Transformer.from_crs("EPSG:2326", "EPSG:4326", always_xy=True)

def convert_coordinates(coords):
    if isinstance(coords[0], list):
        return [convert_coordinates(coord) for coord in coords]
    else:
        lng, lat = transformer.transform(coords[0], coords[1])
        return [lng, lat]

def convert_geometry(geometry):
    if geometry['type'] == 'Polygon':
        geometry['coordinates'] = [convert_coordinates(ring) for ring in geometry['coordinates']]
    elif geometry['type'] == 'MultiPolygon':
        geometry['coordinates'] = [[convert_coordinates(ring) for ring in polygon] for polygon in geometry['coordinates']]
    return geometry

with open('MHE_21C_converted.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for feature in data['features']:
    if feature['geometry']:
        feature['geometry'] = convert_geometry(feature['geometry'])

with open('MHE_21C_wgs84.geojson', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

print("Converted to WGS84: MHE_21C_wgs84.geojson")