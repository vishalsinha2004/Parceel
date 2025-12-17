import requests

def get_ride_details(pickup_coords, dropoff_coords):
    """
    Calculates distance AND returns the route shape (geometry).
    """
    base_url = "http://router.project-osrm.org/route/v1/driving"
    
    # Format: {lon},{lat};{lon},{lat}
    coords = f"{pickup_coords[0]},{pickup_coords[1]};{dropoff_coords[0]},{dropoff_coords[1]}"
    
    # NEW: We added 'overview=full' and 'geometries=geojson' to get the shape
    url = f"{base_url}/{coords}?overview=full&geometries=geojson"

    try:
        response = requests.get(url)
        data = response.json()
        
        if data['code'] == 'Ok':
            route = data['routes'][0]
            distance_meters = route['distance']
            distance_km = distance_meters / 1000
            
            # The Shape of the road
            geometry = route['geometry']
            
            # Pricing Logic
            price = 50 + (distance_km * 15)
            
            return round(distance_km, 2), round(price, 2), geometry
            
    except Exception as e:
        print(f"Error calculating distance: {e}")
    
    return 0.0, 0.0, None