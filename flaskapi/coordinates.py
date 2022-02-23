from geopy.geocoders import Nominatim

def get_lat_lon(city):
  address = city
  geolocator = Nominatim(user_agent="Your_Name")
  location = geolocator.geocode(address)
  if location = None:
    return None, None
  return location.latitude, location.longitude 