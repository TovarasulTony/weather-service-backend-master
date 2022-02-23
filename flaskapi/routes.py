from flaskapi import app
from flask import jsonify
from flaskapi.coordinates import get_lat_lon

@app.route("/ping")
def ping():
  return jsonify({
    "name": "weatherservice",
    "status": "ok",
    "version": "1.0.0"
  })


@app.route("/forecast/<string:city>")
def forecast(city):
  lat, lon = get_lat_lon(city)
  print(lat)
  print(lon)
  return jsonify({
    "lat": lat,
    "lon": lon,
    "version": "1.0.0"
  })