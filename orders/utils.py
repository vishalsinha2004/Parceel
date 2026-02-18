import requests
# orders/utils.py

def get_ride_details(pickup_coords, dropoff_coords):
    base_url = "http://router.project-osrm.org/route/v1/driving"
        
    # OSRM expects: [longitude, latitude]
    coords = f"{pickup_coords[0]},{pickup_coords[1]};{dropoff_coords[0]},{dropoff_coords[1]}"
    url = f"{base_url}/{coords}?overview=full&geometries=geojson"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if data.get('code') == 'Ok':
            route = data['routes'][0]
            distance_km = route['distance'] / 1000
            geometry = route['geometry']
            
            # Base price 50 + 15 per km
            price = 50 + (distance_km * 15)
            return round(distance_km, 2), round(price, 2), geometry
            
    except Exception as e:
        print(f"OSRM Error: {e}")
    
    # Fallback if API is down or coordinates are wrong
    # Return a default distance and a minimum base price of 50
    return 0.0, 50.0, None