from flaskapi import app
from flask import jsonify, request
from flaskapi.coordinates import get_lat_lon
from datetime import timezone
from dateutil import parser as time_parser
from flaskapi.enums import API_CALL_TYPE

import pycurl
import certifi
import json
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
  print(my_json)
  return my_json

def find_clouds(weather):
  for element in weather:
    if element["main"] == "Clouds":
      return element["description"]

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
  if at != None:
    yourdate = time_parser.isoparse(at.replace(" ", "+")) # dirty hack, I don't know how to fix this or if this breaks something else :(
    timestamp_arg = yourdate.replace(tzinfo=timezone.utc).timestamp()
    print(timestamp_arg)
    lat, lon = get_lat_lon(city)
    if lat == None:
      return jsonify({
        "error": "Cannot find country '" + city + "'",
        "error_code": "country_not_found"
      }), 404
    return_json = make_api_call(lat, lon, API_CALL_TYPE.Date)
    return_json = json.loads(return_json)
    if return_json["daily"][0]["dt"] > timestamp_arg:
      return jsonify({
        "error": "Date is in the past",
        "error_code": "invalid date"
      }), 404
    one_day_offset = 86400
    for ele in return_json["daily"]:
      if timestamp_arg >= ele["dt"] and timestamp_arg < ele["dt"] + one_day_offset:
        return jsonify({
          str(ele["weather"][0]["main"]): str(ele["weather"][0]["description"]),
          "humidity": str(round(ele["humidity"], 2)) + "%",
          "pressure": str(round(ele["pressure"], 2)) + " hPa",
          "temperature": str(round(ele["temp"]["day"] - 273.15, 1)) + "C"
        })
    return jsonify({
        "error": "Date is further in the future than supported",
        "error_code": "invalid date"
      }), 404

  lat, lon = get_lat_lon(city)
  if lat == None:
    return jsonify({
      "error": "Cannot find country '" + city + "'",
      "error_code": "country_not_found"
    }), 404

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