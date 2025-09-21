// Initialize the map
var map = L.map('map').setView([28.7041, 77.1025], 10);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Example shelters
var shelters = [
  {name: "Shelter A", lat: 28.7041, lon: 77.1025},
  {name: "Shelter B", lat: 28.5355, lon: 77.3910}
];

// Add markers
shelters.forEach(shelter => {
  L.marker([shelter.lat, shelter.lon]).addTo(map)
    .bindPopup(shelter.name);
});
