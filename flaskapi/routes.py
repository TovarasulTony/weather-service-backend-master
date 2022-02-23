@app.route("/")
@app.route("/ping")
def home():
    return "200"