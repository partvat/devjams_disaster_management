import requests
import json
import csv
import time
import os

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
BBOX = (6.7, 68.7, 35.5, 97.4)  # south, west, north, east

def fetch_osm_shelters():
    query = f"""
    [out:json][timeout:180];
    (
      node["emergency"="shelter"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});
      node["amenity"="shelter"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});
      way["emergency"="shelter"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});
      way["amenity"="shelter"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});
    );
    out center;
    """
    for attempt in range(3):
        try:
            resp = requests.post(OVERPASS_URL, data={'data': query}, timeout=300)
            resp.raise_for_status()
            data = resp.json()
            results = []
            for el in data.get('elements', []):
                tags = el.get('tags', {})
                name = tags.get('name') or tags.get('ref') or "unnamed shelter"
                if el['type'] == 'node':
                    lat, lon = el.get('lat'), el.get('lon')
                else:
                    center = el.get('center', {})
                    lat, lon = center.get('lat'), center.get('lon')
                if lat and lon:
                    results.append({
                        'name': name,
                        'latitude': lat,
                        'longitude': lon
                    })
            return results
        except Exception as e:
            print(f"Overpass attempt {attempt+1} failed: {e}")
            time.sleep(10)
    return []

def fetch_official_shelters():
    # Currently placeholder; no official URL supplied
    return []

def merge_shelter_data(osm_list, official_list):
    merged, seen = [], set()
    for item in osm_list + official_list:
        key = (round(item['latitude'], 4), round(item['longitude'], 4), item['name'].strip().lower())
        if key not in seen:
            seen.add(key)
            merged.append(item)
    return merged

def main():
    print("Fetching OSM shelters...")
    osm = fetch_osm_shelters()
    print(f"Fetched {len(osm)} shelters from OSM")

    official = fetch_official_shelters()
    print(f"Fetched {len(official)} official shelters")

    merged = merge_shelter_data(osm, official)
    print(f"Total shelters: {len(merged)}")

    if not merged:
        print("⚠️ No data fetched. File will not be overwritten.")
        return

    # Ensure file is written to Desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    out_filename = os.path.join(desktop_path, "Shelter_data_out_india.json")

    with open(out_filename, 'w', encoding='utf-8') as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    print(f"[OK] Wrote {len(merged)} shelters to {out_filename}")
    print("Sample of first 5 shelters:", merged[:5])

if __name__ == "__main__":
    main()
