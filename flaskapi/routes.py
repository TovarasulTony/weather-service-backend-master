from flaskapi import app

@app.route("/ping")
def home():
  return jsonify({
    "name": "weatherservice",
    "status": "ok",
    "version": "1.0.0"
  })