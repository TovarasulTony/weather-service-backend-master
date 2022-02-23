import pycurl
import certifi
from io import BytesIO

def make_api_call(lat, lon, call_type):
  buffer = BytesIO()
  c = pycurl.Curl()

  if call_type == API_CALL_TYPE.No_Date:
    c.setopt(c.URL, 'api.openweathermap.org/data/2.5/weather?lat=' + str(lat) + '&lon=' + str(lon) + '&appid=' + 'a380c85701c2082a4ac12ec49f670631')
  elif call_type == API_CALL_TYPE.Date:
    c.setopt(c.URL, 'https://api.openweathermap.org/data/2.5/onecall?lat=' + str(lat) + '&lon=' + str(lon) + '&exclude=current,minutely,hourly,alerts&appid=' + 'a380c85701c2082a4ac12ec49f670631')
  else:
    return None

  c.setopt(c.WRITEDATA, buffer)
  c.setopt(c.CAINFO, certifi.where())
  c.perform()
  c.close()
  body = buffer.getvalue()
  my_json = buffer.getvalue().decode('utf8')
  return my_json