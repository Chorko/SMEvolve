import requests
import folium

# Replace with your Google Maps API Key
API_KEY = "AIzaSyBPeGrA8uU6NTr0tu-pXuC2lOQ8xBvEPoQ"

def get_route(origin, destination):
    url = f"https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "key": API_KEY,
        "mode": "driving",
        "departure_time": "now",
        "traffic_model": "pessimistic",
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data["status"] == "OK":
        return data["routes"][0]["overview_polyline"]["points"]
    else:
        print("Error:", data["status"])
        return None

def decode_polyline(polyline):
    # Decode polyline into coordinates
    points = []
    index, lat, lng = 0, 0, 0

    while index < len(polyline):
        result, shift = 0, 0
        while True:
            b = ord(polyline[index]) - 63
            index += 1
            result |= (b & 0x1f) << shift
            shift += 5
            if b < 0x20:
                break
        lat += ~(result >> 1) if result & 1 else result >> 1

        result, shift = 0, 0
        while True:
            b = ord(polyline[index]) - 63
            index += 1
            result |= (b & 0x1f) << shift
            shift += 5
            if b < 0x20:
                break
        lng += ~(result >> 1) if result & 1 else result >> 1

        points.append((lat / 1e5, lng / 1e5))
    return points

def plot_route(route_points, origin, destination):
    # Create a folium map centered on the route
    start_coords = route_points[0]
    route_map = folium.Map(location=start_coords, zoom_start=13)
    
    # Plot the route
    folium.PolyLine(route_points, color="blue", weight=5, opacity=0.7).add_to(route_map)
    
    # Add markers for origin and destination
    folium.Marker(location=route_points[0], popup="Origin").add_to(route_map)
    folium.Marker(location=route_points[-1], popup="Destination").add_to(route_map)
    
    # Save the map to an HTML file
    route_map.save("route_map.html")
    print("Map saved as route_map.html!")

# Inputs
origin = "Times Square, New York, NY"
destination = "Central Park, New York, NY"

# Fetch and decode the route
encoded_polyline = get_route(origin, destination)
if encoded_polyline:
    route_coords = decode_polyline(encoded_polyline)
    plot_route(route_coords, origin, destination)
