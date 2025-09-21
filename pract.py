import requests
import json
import time

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
LAT_STEP = 20
LON_STEP = 20

def generate_bboxes():
    bboxes = []
    for lat_min in range(-90, 90, LAT_STEP):
        for lon_min in range(-180, 180, LON_STEP):
            lat_max = min(lat_min + LAT_STEP, 90)
            lon_max = min(lon_min + LON_STEP, 180)
            bboxes.append((lat_min, lon_min, lat_max, lon_max))
    return bboxes

def overpass_query(bbox):
    lat_min, lon_min, lat_max, lon_max = bbox
    query = f"""
    [out:json][timeout:900];
    (
      node["emergency"="shelter"]({lat_min},{lon_min},{lat_max},{lon_max});
      node["amenity"="shelter"]({lat_min},{lon_min},{lat_max},{lon_max});
      way["emergency"="shelter"]({lat_min},{lon_min},{lat_max},{lon_max});
      way["amenity"="shelter"]({lat_min},{lon_min},{lat_max},{lon_max});
      relation["emergency"="shelter"]({lat_min},{lon_min},{lat_max},{lon_max});
      relation["amenity"="shelter"]({lat_min},{lon_min},{lat_max},{lon_max});
    );
    out center;
    """
    return query

def fetch_shelters():
    bboxes = generate_bboxes()
    all_shelters = []

    for idx, bbox in enumerate(bboxes):
        print(f"Fetching bbox {idx+1}/{len(bboxes)}: {bbox}")
        query = overpass_query(bbox)
        try:
            response = requests.post(OVERPASS_URL, data={"data": query})
            response.raise_for_status()
            data = response.json()
            
            for element in data['elements']:
                shelter = {
                    "id": element.get("id"),
                    "type": element.get("type"),
                    "lat": element.get("lat") or element.get("center", {}).get("lat"),
                    "lon": element.get("lon") or element.get("center", {}).get("lon"),
                    "tags": element.get("tags", {})
                }
                all_shelters.append(shelter)
        except Exception as e:
            print(f"Error fetching bbox {bbox}: {e}")
        
        # Avoid hammering Overpass servers
        time.sleep(5)

    # Remove duplicates
    unique_shelters = {s['id']: s for s in all_shelters}.values()
    return list(unique_shelters)

def save_to_json(shelters, filename="disaster_shelters.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(shelters, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(shelters)} shelters to {filename}")

if __name__ == "__main__":
    shelters = fetch_shelters()
    save_to_json(shelters)







