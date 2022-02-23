from flaskapi import app
from flask import jsonify

@app.route("/ping")
def home():
  return jsonify({
    "name": "weatherservice",
    "status": "ok",
    "version": "1.0.0"
  })