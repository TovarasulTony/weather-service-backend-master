import pycurl
import certifi
import json
from io import BytesIO

with open("flaskapi/config.json") as jsonFile:
  jsonConfig = json.load(jsonFile)
  jsonFile.close()
SERVER_IP = jsonConfig["IP"]
PORT_IP = jsonConfig["PORT"]
USERNAME_BA = jsonConfig["USERNAME_BA"]
PASS_BA = jsonConfig["PASS_BA"]
BASIC_URL = "http://" + SERVER_IP + ":" + str(PORT_IP) + "/"


def make_api_call(route, ba_auth=True, city=None, at=None):
  buffer = BytesIO()
  c = pycurl.Curl()
  if route == "ping":
    print(BASIC_URL + "ping")
    c.setopt(c.URL, BASIC_URL + "ping")
  elif route == "forecast" and at == None:
    c.setopt(c.URL, BASIC_URL + "forecast/" + city)
  elif route == "forecast" and at != None:
    c.setopt(c.URL, BASIC_URL + "forecast/" + city + "/?at=" + at)

  if ba_auth == True:
    c.setopt(c.HTTPAUTH, c.HTTPAUTH_BASIC)
    c.setopt(c.USERPWD, '%s:%s' %(USERNAME_BA, PASS_BA))
  c.setopt(c.HTTPHEADER, ['Accept: application/json'])
  c.setopt(c.WRITEDATA, buffer)
  c.setopt(c.CAINFO, certifi.where())
  c.perform()
  c.close()
  body = buffer.getvalue()
  my_json = buffer.getvalue().decode('utf8')
  return my_json

def test_ping():
  response_json = make_api_call("ping")
  print(response_json)
  response_json = json.loads(response_json)
  if response_json["name"] != "weatherservice":
    return False
  if response_json["status"] != "ok":
    return False
  if response_json["version"] != "1.0.0":
    return False
  return True

def test_forecast():
  response_json = make_api_call(route="forecast", city="london")
  response_json = json.loads(response_json)
  for elem in response_json:
    print(response_json[elem])
  if response_json["humidity"] != None or len(response_json["humidity"]) <= 1 or response_json["humidity"][-1] != "%":
    return False
  if response_json["pressure"] != None or len(response_json["pressure"]) <= 4 or response_json["pressure"][-4:0] != " hPa":
    return False
  if response_json["temperature"] != None or len(response_json["temperature"]) <= 1 or response_json["temperature"][-1] != "C":
    return False
  return True

def test_forecast_ba():
  response_json = make_api_call(route="forecast", ba_auth=False)
  response_json = json.loads(response_json)
  for elem in response_json:
    print(response_json[elem])
  if response_json["error"] != "You are not authorized for access" or response_json["error_code"] != "wrong_credentials":
    return False
  return True

def test_forecast_at():
  response_json = make_api_call(route="forecast", city="london", at="2022-02-26")
  response_json = json.loads(response_json)
  for elem in response_json:
    print(response_json[elem])
  if response_json["humidity"] != None or len(response_json["humidity"]) <= 1 or response_json["humidity"][-1] != "%":
    return False
  if response_json["pressure"] != None or len(response_json["pressure"]) <= 4 or response_json["pressure"][-4:0] != " hPa":
    return False
  if response_json["temperature"] != None or len(response_json["temperature"]) <= 1 or response_json["temperature"][-1] != "C":
    return False
  return True

def test_all():
  print("-----")
  print("test_ping:")
  print(test_ping())
  print("-----")

  print("-----")
  print("test_forecast:")
  print(test_forecast())
  print("-----")
  
  print("-----")
  print("test_forecast_ba:")
  print(test_forecast_ba())
  print("-----")
  
  print("-----")
  print("test_forecast_at:")
  print(test_forecast_at())
  print("-----")


test_all()