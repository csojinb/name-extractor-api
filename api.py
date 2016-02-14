import os

from flask import Flask, request, jsonify
from schematics.models import Model
from schematics.types import StringType
from schematics.types.compound import ListType, ModelType

from name_extractor import extract_person_names

DEVELOPMENT_MODE = os.environ.get('DEVELOP') == 'true'

app = Flask(__name__)


class RequestData(Model):
    text = StringType(required=True)


@app.route('/extract-names/', methods=['POST'])
def extract_names():
    request_data = RequestData(request.json)
    request_data.validate()

    names = [{"name": name, "gender": ""}
             for name in extract_person_names(request_data.text)]

    return jsonify({"names": names})


if __name__ == '__main__':
    app.run(debug=DEVELOPMENT_MODE)
