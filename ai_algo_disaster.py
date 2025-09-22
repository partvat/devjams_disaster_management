import requests
import numpy as np
from sklearn.cluster import KMeans
import json
import os

NASA_API = "https://eonet.gsfc.nasa.gov/api/v3/events"
WEATHER_API = "https://api.open-meteo.com/v1/forecast"

# Step 1: Fetch NASA data
def fetch_nasa_data():
    try:
        resp = requests.get(NASA_API)
        data = resp.json()
        coords = []
        for ev in data.get("events", []):
            for geom in ev.get("geometry", []):
                if geom["type"] == "Point":
                    lon, lat = geom["coordinates"]
                    coords.append([lat, lon])
        return np.array(coords) if coords else np.empty((0, 2))
    except Exception as e:
        print("NASA API error:", e)
        return np.empty((0, 2))

# Step 2: Weather risk (free via Open-Meteo)
def weather_risk(lat, lon):
    try:
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "precipitation,windspeed_10m,cloudcover"
        }
        resp = requests.get(WEATHER_API, params=params).json()
        current = resp.get("current", {})
        rain = current.get("precipitation", 0)
        wind = current.get("windspeed_10m", 0)
        clouds = current.get("cloudcover", 0)

        # Simple scoring logic
        risk = 1.0
        if rain > 5:  # heavy rain
            risk += 1.0
        if wind > 40:  # stormy winds
            risk += 1.0
        if clouds > 80:  # very cloudy (storm build-up)
            risk += 0.5
        return risk
    except:
        return 1.0

# Step 3: Clustering
def predict_hotspots(coords, top_n=5):
    if len(coords) < top_n:
        return coords
    kmeans = KMeans(n_clusters=top_n, random_state=42, n_init=10)
    kmeans.fit(coords)
    return kmeans.cluster_centers_

# Step 4: Main pipeline
if __name__ == "__main__":
    coords = fetch_nasa_data()
    if coords.shape[0] == 0:
        print("No data available.")
    else:
        hotspots = predict_hotspots(coords, top_n=5)
        output_data = []
        for i, h in enumerate(hotspots, 1):
            risk = weather_risk(h[0], h[1])
            h_pred = h + np.random.normal(0, 0.5, size=2)  # tiny jitter
            output_data.append({
                "rank": i,
                "latitude": round(float(h_pred[0]), 4),
                "longitude": round(float(h_pred[1]), 4),
                "risk_score": round(float(risk), 2)
            })

        # Ensure file is written to samelocation as existing file
        out_filename = "ai_output.json"
        if not os.path.isabs(out_filename):
            out_filename = os.path.join(os.getcwd(), out_filename)

        with open(out_filename, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"Predicted high-risk hotspots saved to {out_filename}")
