from geopy.geocoders import Nominatim

def get_lat_lon(city):
  address = city
  geolocator = Nominatim(user_agent="Your_Name")
  location = geolocator.geocode(address)
  print(55555555)
  print(location.address)
  return location.latitude, location.longitude 