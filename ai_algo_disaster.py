import requests
import numpy as np
from sklearn.cluster import KMeans
import json
import os

# Step 1: Fetch data (NASA EONET API for global natural events)
API_URL = "https://eonet.gsfc.nasa.gov/api/v3/events"

def fetch_data():
    try:
        resp = requests.get(API_URL)
        data = resp.json()
        coords = []
        for ev in data.get("events", []):
            for geom in ev.get("geometry", []):
                if geom["type"] == "Point":
                    lon, lat = geom["coordinates"]
                    coords.append([lat, lon])
        return np.array(coords) if coords else np.empty((0,2))
    except Exception as e:
        print("API error:", e)
        return np.empty((0,2))

# Step 2: Train simple clustering model to find hotspots
def predict_hotspots(coords, top_n=5):
    if len(coords) < top_n:
        return coords
    kmeans = KMeans(n_clusters=top_n, random_state=42, n_init=10)
    kmeans.fit(coords)
    return kmeans.cluster_centers_

# Step 3: Main AI "prediction"
if __name__ == "__main__":
    coords = fetch_data()
    if coords.shape[0] == 0:
        print("No data available.")
    else:
        hotspots = predict_hotspots(coords, top_n=5)
        output_data = []
        for i, h in enumerate(hotspots, 1):
            h_pred = h + np.random.normal(0, 0.5, size=2)  # Add tiny random noise
            output_data.append({
                "rank": i,
                "latitude": round(float(h_pred[0]), 4),
                "longitude": round(float(h_pred[1]), 4)
            })

        # Ensure file is written to same location as existing file
        out_filename = "ai_output.json"
        if not os.path.isabs(out_filename):
            out_filename = os.path.join(os.getcwd(), out_filename)

        with open(out_filename, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"Predicted next disaster hotspots saved to {out_filename}")
