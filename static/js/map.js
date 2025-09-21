// Initialize map
const urlParams = new URLSearchParams(window.location.search);
const role = urlParams.get('role');

const map = L.map("map").setView([20.5937, 78.9629], 5);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: '&copy; OpenStreetMap contributors',
}).addTo(map);


