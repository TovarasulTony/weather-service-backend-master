import pycurl
import certifi
from io import BytesIO
import json

from flaskapi.enums import API_CALL_TYPE


with open("flaskapi/config.json") as jsonFile:
  jsonObject = json.load(jsonFile)
  jsonFile.close()
API_KEY = jsonObject["API_KEY"]

def make_api_call(lat, lon, call_type):
  buffer = BytesIO()
  c = pycurl.Curl()

  if call_type == API_CALL_TYPE.No_Date:
    c.setopt(c.URL, 'api.openweathermap.org/data/2.5/weather?lat=' + str(lat) + '&lon=' + str(lon) + '&appid=' + API_KEY)
  elif call_type == API_CALL_TYPE.Date:
    c.setopt(c.URL, 'https://api.openweathermap.org/data/2.5/onecall?lat=' + str(lat) + '&lon=' + str(lon) + '&exclude=current,minutely,hourly,alerts&appid=' + API_KEY)
  else:
    return None

  c.setopt(c.WRITEDATA, buffer)
  c.setopt(c.CAINFO, certifi.where())
  c.perform()
  c.close()
  body = buffer.getvalue()
  my_json = buffer.getvalue().decode('utf8')
  return my_json