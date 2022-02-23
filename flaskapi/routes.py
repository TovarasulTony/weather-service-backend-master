from flaskapi import app
from flask import jsonify
from coordinates import get_lat_lon

@app.route("/ping")
def ping():
  return jsonify({
    "name": "weatherservice",
    "status": "ok",
    "version": "1.0.0"
  })


@app.route("/forecast/<str:city>")
def forecast(city):
  lat, lon = get_lat_lon(city)
  return jsonify({
    "lat": lat,
    "lon": lon,
    "version": "1.0.0"
  })