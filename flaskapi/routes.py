import json

from flaskapi import app
from flask import jsonify, request
from flaskapi.coordinates import get_lat_lon
from flaskapi.pycurl_wrapper import make_api_call
from datetime import timezone
from dateutil import parser as time_parser
from flaskapi.enums import API_CALL_TYPE

CELSIUS_KELVIN_OFFSET = 273.15

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
def forecast(city):
  at = request.args.get('at', type=str)
  lat, lon = get_lat_lon(city)

  if lat == None:
    return jsonify({
      "error": "Cannot find country/region/city '" + city + "'",
      "error_code": "country_not_found"
    }), 404

  if at != None:
    return handle_at_arg_case(at, lat, lon)
  else:
    return_json = make_api_call(lat, lon, API_CALL_TYPE.No_Date)
    return_json = json.loads(return_json)
    return jsonify({
      str(return_json["weather"][0]["main"]): str(return_json["weather"][0]["description"]),
      "humidity": str(round(return_json["main"]["humidity"], 2)) + "%",
      "pressure": str(round(return_json["main"]["pressure"], 2)) + " hPa",
      "temperature": str(round(return_json["main"]["temp"] - 273.15, 1)) + "C"
    })

@app.errorhandler(500)
def internal_error(error):
  return jsonify({
    "error": "Something went wrong",
    "error_code": "internal_server_error"
  }), 500

def handle_at_arg_case(at, lat, lon):
  yourdate = time_parser.isoparse(at.replace(" ", "+")) # dirty hack, I don't know how to fix this or if this breaks something else :(
  timestamp_arg = yourdate.replace(tzinfo=timezone.utc).timestamp()
  return_json = make_api_call(lat, lon, API_CALL_TYPE.Date)
  return_json = json.loads(return_json)
  ONE_DAY_UNIX_OFFSET = 86400

  if return_json["daily"][0]["dt"] - ONE_DAY_UNIX_OFFSET > timestamp_arg:
    return jsonify({
      "error": "Date is in the past",
      "error_code": "invalid date"
    }), 404

  for ele in return_json["daily"]:
    if timestamp_arg >= ele["dt"] - ONE_DAY_UNIX_OFFSET and timestamp_arg <= ele["dt"]:
      return jsonify({
        str(ele["weather"][0]["main"]): str(ele["weather"][0]["description"]),
        "humidity": str(round(ele["humidity"], 2)) + "%",
        "pressure": str(round(ele["pressure"], 2)) + " hPa",
        "temperature": str(round(ele["temp"]["day"] - CELSIUS_KELVIN_OFFSET, 1)) + "C"
      })

  return jsonify({
      "error": "Date is further in the future than supported",
      "error_code": "invalid date"
    }), 404