from flaskapi import app
import json


if __name__ == '__main__':
  with open("flaskapi/config.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()
  app.run(host=jsonObject["IP"], port=jsonObject["PORT"], debug=True)
