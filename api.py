import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from schematics.models import Model
from schematics.types import StringType
from schematics.types.compound import ListType, ModelType
from unidecode import unidecode

from name_extractor import extract_person_names
from genderizer import predict_gender

DEVELOPMENT_MODE = os.environ.get('DEVELOP') == 'true'
PORT = int(os.environ.get('PORT', 5000))

app = Flask(__name__)
CORS(app)


class RequestData(Model):
    text = StringType(required=True)


@app.route('/extract-names/', methods=['POST'])
def extract_names():
    request_data = RequestData(request.json)
    request_data.validate()

    names = [{"name": name, "gender": predict_gender(name)}
             for name in extract_person_names(unidecode(request_data.text))]

    return jsonify({"names": names})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=DEVELOPMENT_MODE, port=PORT, threaded=True)
