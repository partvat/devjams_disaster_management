async function initRole() {
  if(role === "rescuers") {
    const layerGroup = L.layerGroup().addTo(map);

    async function loadRescuees() {
      const res = await fetch('/get-locations');
      const locations = await res.json();
      layerGroup.clearLayers();
      locations.forEach(loc => {
        L.marker([loc.lat, loc.lng], { 
          icon: L.icon({ 
            iconUrl: 'https://cdn-icons-png.flaticon.com/512/565/565547.png', 
            iconSize: [35,35] 
          }) 
        }).addTo(layerGroup).bindPopup("<b>To Be Rescued</b>");
      });
    }

    await loadRescuees();
    setInterval(loadRescuees, 5000);

  } else if(role === "toRescue") {
    if(navigator.geolocation){
      navigator.geolocation.getCurrentPosition(pos => {
        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;
        map.setView([lat, lng], 15);

        L.marker([lat, lng], { 
          icon: L.icon({ iconUrl: 'https://cdn-icons-png.flaticon.com/512/565/565547.png', iconSize: [35,35] }) 
        }).addTo(map).bindPopup("<b>You (To Be Rescued)</b>").openPopup();

        fetch('/store-location', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ lat, lng, role })
        });

      }, () => alert("Unable to fetch location"));
    } else alert("Geolocation not supported");
  }
}

initRole();

