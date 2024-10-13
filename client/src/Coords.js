import React, { useState, useEffect, useRef, useCallback } from "react";
import maplibregl from "maplibre-gl";
import Navbar from "./Navbar";

const Coords = () => {
    const [coords, setCoords] = useState([]);
    const [isSatellite, setIsSatellite] = useState(false);
    const mapContainerRef = useRef(null);
    const mapRef = useRef(null);
    const markersRef = useRef(new Map());

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
            mapRef.current = new maplibregl.Map({
                container: mapContainerRef.current,
                style: isSatellite
                    ? 'https://api.maptiler.com/maps/hybrid/style.json?key=32wiXpnDZ4ucpuWo6b7h'
                    : 'https://api.maptiler.com/maps/streets-v2/style.json?key=32wiXpnDZ4ucpuWo6b7h',
                zoom: 1.33,
                center: [10, 25],
            });

            mapRef.current.addControl(new maplibregl.NavigationControl(), 'top-right');
            mapRef.current.on('zoom', debounce(updateMarkerSize, 200));
        } else {
            mapRef.current.setStyle(
                isSatellite
                    ? 'https://api.maptiler.com/maps/hybrid/style.json?key=32wiXpnDZ4ucpuWo6b7h'
                    : 'https://api.maptiler.com/maps/streets-v2/style.json?key=32wiXpnDZ4ucpuWo6b7h'
            );
        }

        markersRef.current.forEach(marker => marker.remove());
        markersRef.current.clear();

        if (coords.length > 0) {
            coords.forEach(({ lat, long, url }) => {
                const el = document.createElement('div');
                el.className = 'marker';
                el.style.backgroundImage = "url('/red_camera.png')";
                el.style.backgroundSize = 'cover';
                el.style.width = '50px';
                el.style.height = '50px';
                el.style.borderRadius = '50%';
                el.style.cursor = 'pointer';

                el.addEventListener('click', () => {
                    window.open(url, '_blank');
                });

                const marker = new maplibregl.Marker({ element: el })
                    .setLngLat([long, lat])
                    .addTo(mapRef.current);

                markersRef.current.set(url, marker);
            });

            updateMarkerSize();
        }
    }, [coords, isSatellite]);

    const updateMarkerSize = useCallback(() => {
        const zoom = mapRef.current.getZoom();
        const newSize = Math.max(15, Math.min(50, zoom * 5));

        markersRef.current.forEach(marker => {
            const markerElement = marker.getElement();
            markerElement.style.width = `${newSize}px`;
            markerElement.style.height = `${newSize}px`;
        });
    }, []);

    const debounce = (func, delay) => {
        let timeoutId;
        return (...args) => {
            if (timeoutId) {
                clearTimeout(timeoutId);
            }
            timeoutId = setTimeout(() => {
                func(...args);
            }, delay);
        };
    };

    const toggleSatellite = () => {
        setIsSatellite(prev => !prev);
    };

    return (
        <div style={{ position: "relative" }}>
            <Navbar isSatellite={isSatellite} toggleSatellite={toggleSatellite} pointCount={coords.length} /> {/* Pass pointCount */}
            <div ref={mapContainerRef} style={{ height: "93vh", width: "100%" }} />
        </div>
    );
};

export default Coords;