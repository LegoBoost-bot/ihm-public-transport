import json
import requests

url = "https://data.gov.il/api/3/action/datastore_search?resource_id=e873e6a2-66c1-494f-a677-f5e77348edb0"

first_req = requests.get(url).json()["result"]

total_entries = first_req["total"]
limit = first_req["limit"]
batches = (total_entries + limit - 1) // limit
print(f"Total entries: {total_entries}. Fetching {batches-1} more batches...")

records = first_req["records"]

assert len(records) == limit or len(records) == total_entries

for i in range(1, batches):
    offset = limit * i
    resp = requests.get(url + f"&offset={offset}").json()["result"]
    records += resp["records"]

print(f"Collected {len(records)} records.")

r = [
    {
        "type": "Feature",
        "properties": {"StationId": r["StationId"]},
        "geometry": {
            "type": "Point",
            "coordinates": [
                r["Long"],
                r["Lat"],
            ],
        },
    }
    for r in records
]

geojson = {"type": "FeatureCollection", "features": r}

with open("source.geojson", "w") as f:
    json.dump(geojson, f, indent=4)
