html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>MapLibre GL Circle Example</title>
    <meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no" />
    <script src="https://unpkg.com/maplibre-gl@1.15.2/dist/maplibre-gl.js"></script>
    <link href="https://unpkg.com/maplibre-gl@1.15.2/dist/maplibre-gl.css" rel="stylesheet" />
    <style>
        body { margin: 0; padding: 0; }
        #map { position: absolute; top: 0; bottom: 0; width: 100%; }
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        var map = new maplibregl.Map({
            container: 'map',
            style: 'https://demotiles.maplibre.org/style.json', // Use MapLibre's demo style
            center: [{center_lon}, {center_lat}],
            zoom: 4
        });

        // Add a circle
        
        map.on('load', () => {
            map.addSource('circle', {
                'type': 'geojson',
                'data': {
                    'type': 'Feature',
                    'properties': {},
                    'geometry': {
                        'type': 'LineString',
                        'coordinates': {circle_coords}
                    }
                }
            });

            map.addLayer({
                'id': 'circle',
                'type': 'line',
                'source': 'circle',
                'paint': {
                    'line-color': '#888888',
                    'line-width': 4
                }
            });
        });
    </script>
</body>
</html>
"""