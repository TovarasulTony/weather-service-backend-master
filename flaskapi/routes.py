import json
from datetime import timezone
from dateutil import parser as time_parser
from flask import jsonify, request
from flask_httpauth import HTTPBasicAuth
from flaskapi import app
from flaskapi.coordinates import get_lat_lon
from flaskapi.pycurl_wrapper import make_api_call
from flaskapi.enums import API_CALL_TYPE
from flaskapi.cache import CacheStruct


with open("flaskapi/config.json") as jsonFile:
  jsonConfig = json.load(jsonFile)
  jsonFile.close()
CELSIUS_KELVIN_OFFSET = 273.15
ONE_DAY_UNIX_OFFSET = 64800
USERNAME_BA = jsonConfig["USERNAME_BA"]
PASS_BA = jsonConfig["PASS_BA"]
cache_struct = CacheStruct()

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
  if username == USERNAME_BA and password == PASS_BA:
    return True
  return False

@app.route("/ping")
@app.route("/ping/")
def ping():
  return jsonify({
    "name": "weatherservice",
    "status": "ok",
    "version": "1.0.0"
  })


@app.route("/forecast/<string:city>")
@app.route("/forecast/<string:city>/")
@auth.login_required
def forecast(city):
  if request.authorization["username"] != USERNAME_BA and request.authorization["password"] != PASS_BA:
      return jsonify({
        "error": "You are not authorized for access",
        "error_code": "wrong_credentials"
      }), 403
  at = request.args.get('at', type=str)
  lat, lon = get_lat_lon(city)

  if lat == None:
    return jsonify({
      "error": "Cannot find country/region/city '" + city + "'",
      "error_code": "country_not_found"
    }), 404

  cached_response, is_cached, cache_id = cache_struct.check_request(city, at)
  if is_cached == True:
    return cached_response

  if at != None:
    return handle_at_arg_case(at, lat, lon, cache_id)
  else:
    response_json = make_api_call(lat, lon, API_CALL_TYPE.No_Date)
    response_json = json.loads(response_json)
    return_json = jsonify({
      str(response_json["weather"][0]["main"]): str(response_json["weather"][0]["description"]),
      "humidity": str(round(response_json["main"]["humidity"], 2)) + "%",
      "pressure": str(round(response_json["main"]["pressure"], 2)) + " hPa",
      "temperature": str(round(response_json["main"]["temp"] - CELSIUS_KELVIN_OFFSET, 1)) + "C"
    })
    cache_struct.cache_response(cache_id, return_json)
    return return_json

@app.errorhandler(500)
def internal_error(error):
  return jsonify({
    "error": "Something went wrong",
    "error_code": "internal_server_error"
  }), 500

@app.errorhandler(403)
def forbidden_access(error):
  return jsonify({
    "error": "You are not authorized for access",
    "error_code": "wrong_credentials"
  }), 403

def handle_at_arg_case(at, lat, lon, cache_id):
  yourdate = time_parser.isoparse(at.replace(" ", "+")) # dirty hack, I don't know how to fix this or if this breaks something else :(
  timestamp_arg = yourdate.replace(tzinfo=timezone.utc).timestamp()
  return_json = make_api_call(lat, lon, API_CALL_TYPE.Date)
  return_json = json.loads(return_json)

  if return_json["daily"][0]["dt"] - ONE_DAY_UNIX_OFFSET > timestamp_arg:
    return jsonify({
      "error": "Date is in the past",
      "error_code": "invalid date"
    }), 404

  for ele in return_json["daily"]:
    if timestamp_arg >= ele["dt"] - ONE_DAY_UNIX_OFFSET and timestamp_arg <= ele["dt"]:
      return_json = jsonify({
        str(ele["weather"][0]["main"]): str(ele["weather"][0]["description"]),
        "humidity": str(round(ele["humidity"], 2)) + "%",
        "pressure": str(round(ele["pressure"], 2)) + " hPa",
        "temperature": str(round(ele["temp"]["day"] - CELSIUS_KELVIN_OFFSET, 1)) + "C"
      })
      cache_struct.cache_response(cache_id, return_json)
      return return_json

  return jsonify({
      "error": "Date is further in the future than supported",
      "error_code": "invalid date"
    }), 404