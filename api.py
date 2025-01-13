import requests
from requests.structures import CaseInsensitiveDict

# Base URL for the Geoapify Places API
url = "https://api.geoapify.com/v2/places?categories=tourism.attraction,tourism.attraction.viewpoint,tourism.attraction.artwork,tourism,tourism.sights&filter=rect:-17.0,35.0,-1.0,21.0&limit=20&apiKey=e0ffa5a008b54f07bbf280839ad36e86"




# Make the GET request
response = requests.get(url)

# Check response status and print results
if response.status_code == 200:
    data = response.json()  # Parse the response as JSON
    # Iterate over the features to print information
    for place in data.get("features", []):
        properties = place.get("properties", {})
        print("Name:", properties.get("name", "Unknown"))
        print("Category:", properties.get("categories", []))
        print("Address:", properties.get("formatted"))
        print("Latitude:", properties.get("lat"))
        print("Longitude:", properties.get("lon"))
        print("-" * 40)
else:
    print(f"Request failed with status code: {response.status_code}")
