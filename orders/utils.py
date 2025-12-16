import requests

def get_ride_details(pickup_coords, dropoff_coords):
    """
    Calculates distance using OSRM (Open Source Routing Machine).
    pickup_coords: tuple (longitude, latitude)
    dropoff_coords: tuple (longitude, latitude)
    """
    # OSRM Public Demo Server URL
    base_url = "http://router.project-osrm.org/route/v1/driving"
    
    # Format: {lon},{lat};{lon},{lat}
    coords = f"{pickup_coords[0]},{pickup_coords[1]};{dropoff_coords[0]},{dropoff_coords[1]}"
    url = f"{base_url}/{coords}?overview=false"

    try:
        response = requests.get(url)
        data = response.json()
        
        if data['code'] == 'Ok':
            distance_meters = data['routes'][0]['distance']
            distance_km = distance_meters / 1000
            
            # Pricing Logic: Base ₹50 + ₹15 per km
            price = 50 + (distance_km * 15)
            
            return round(distance_km, 2), round(price, 2)
    except Exception as e:
        print(f"Error calculating distance: {e}")
    
    return 0.0, 0.0 # Return 0 if fails