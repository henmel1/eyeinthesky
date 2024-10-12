import React, { useState, useEffect, useRef } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";

const Coords = () => {
  const [coords, setCoords] = useState([]);
  const mapContainerRef = useRef(null);
  const mapRef = useRef(null); // To store the map instance

  useEffect(() => {
    const fetchCoords = async () => {
      try {
        const response = await fetch('/api/coords');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setCoords(data.coords);
      } catch (error) {
        console.error('Error fetching coords:', error);
      }
    };

    fetchCoords();
  }, []);

  useEffect(() => {
    if (!mapRef.current) {
      // Initialize the map only once
      mapRef.current = new maplibregl.Map({
        container: mapContainerRef.current,
        style: 'https://api.maptiler.com/maps/streets-v2/style.json?key=32wiXpnDZ4ucpuWo6b7h',
        zoom: 1.75,
        center: [10, 30],
      });

      mapRef.current.addControl(new maplibregl.NavigationControl(), 'top-right');

      // Update marker size on zoom
      mapRef.current.on('zoom', updateMarkerSize);
    }

    if (coords.length > 0) {
      // Add markers after the map has been initialized
      coords.forEach(({ lat, long, url }) => {
        const el = document.createElement('div');
        el.className = 'marker';
        el.style.backgroundImage = "url('https://img.freepik.com/premium-vector/computer-web-cam-with-standing-clipart_251822-508.jpg')";
        el.style.backgroundSize = 'cover';
        el.style.width = '50px';
        el.style.height = '50px';
        el.style.borderRadius = '50%';
        el.style.cursor = 'pointer';

        el.addEventListener('click', () => {
          window.open(url, '_blank'); // Open in a new tab
        });

        new maplibregl.Marker({ element: el })
          .setLngLat([long, lat])
          .addTo(mapRef.current);
      });

      // Update marker size initially
      updateMarkerSize();
    }
  }, [coords]); // Re-run this effect when the coords state changes

  // Function to update marker size based on zoom level
  const updateMarkerSize = () => {
    const zoom = mapRef.current.getZoom();
    // Calculate the new size based on zoom (max size 50px, scale down as zoom decreases)
    const newSize = Math.max(15, Math.min(50, zoom * 5)); // Adjust scaling factor as needed

    document.querySelectorAll('.marker').forEach(marker => {
      marker.style.width = `${newSize}px`;
      marker.style.height = `${newSize}px`;
    });
  };

  return <div ref={mapContainerRef} style={{ height: "100vh", width: "100%" }} />;
};

function App() {
  return (
    <div>
      <Coords />
    </div>
  );
}

export default App;
