from flask import Flask, request, jsonify, render_template
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
LOCATIONS_FILE = 'user_locations.json'

# Ensure the locations file exists
if not os.path.exists(LOCATIONS_FILE):
    with open(LOCATIONS_FILE, 'w') as f:
        json.dump([], f)

# Serve landing page
@app.route('/')
def landing():
    return render_template('landing.html')

# Serve map page
@app.route('/map')
def map_page():
    return render_template('map.html')

# Store location for To Be Rescued users
@app.route('/store-location', methods=['POST'])
def store_location():
    data = request.get_json()
    if not data or data.get('role') != 'toRescue':
        return jsonify({'success': False, 'message': 'Only To Be Rescued users are stored'}), 200
    if 'lat' not in data or 'lng' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    with open(LOCATIONS_FILE, 'r') as f:
        locations = json.load(f)

    locations.append({'lat': data['lat'], 'lng': data['lng']})

    with open(LOCATIONS_FILE, 'w') as f:
        json.dump(locations, f, indent=2)

    return jsonify({'success': True}), 200

# Get all saved To Be Rescued locations
@app.route('/get-locations', methods=['GET'])
def get_locations():
    with open(LOCATIONS_FILE, 'r') as f:
        locations = json.load(f)
    return jsonify(locations)
# Run SOS service (for button trigger)
@app.route('/run-sos', methods=['GET'])
def run_sos():
    return jsonify({"message": "SOS service triggered successfully!"})
if __name__ == '__main__':
    app.run(debug=True)
    

