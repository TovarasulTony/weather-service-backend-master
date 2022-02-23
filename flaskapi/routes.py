from flaskapi import app
from flask import jsonify
from flaskapi.coordinates import get_lat_lon

import flaskapi.pycurl.python.curl as pycurl
import certifi
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
  print(body.decode('iso-8859-1'))

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
  lat, lon = get_lat_lon(city)
  make_api_call(lat, lon)
  return jsonify({
    "lat": lat,
    "lon": lon,
    "version": "1.0.0"
  })