from flaskapi import app
from flask import jsonify, request
from flaskapi.coordinates import get_lat_lon

import pycurl
import certifi
import json
from io import BytesIO



def make_api_call(lat, lon):
  buffer = BytesIO()
  c = pycurl.Curl()
  c.setopt(c.URL, 'api.openweathermap.org/data/2.5/weather?lat=' + str(lat) + '&lon=' + str(lon) + '&appid=' + 'a380c85701c2082a4ac12ec49f670631')
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
@app.route("/ping")
def ping():
  return jsonify({
    "name": "weatherservice",
    "status": "ok",
    "version": "1.0.0"
  })


@app.route("/forecast/<string:city>")
@app.route("/forecast/<string:city>/")
def forecast(city):
  at = request.args.get('at')
  lat, lon = get_lat_lon(city)
  if lat == None:
    return jsonify({
      "error": "Cannot find country '" + city + "'",
      "error_code": "country_not_found"
    }), 404

  return_json = make_api_call(lat, lon)
  return_json = json.loads(return_json)
  return jsonify({
    "clouds": find_clouds(return_json["weather"]),
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