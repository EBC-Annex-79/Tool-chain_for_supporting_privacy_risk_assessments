import os
import sys

current_path = os.path.abspath('.')
sys.path.append(current_path)

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
from Framework.Run import execute_template

app = Flask(__name__)
# app.config["DEBUG"] = True

# enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# app.config['CORS_HEADERS'] = 'Content-Type',


@cross_origin()
@app.route('/', methods=['GET'])
@cross_origin()
def home():
    return "<h1>Privacy risk anslyses</h1> <p>Use endpoint POST /api/v1 </p>"


@cross_origin()
@app.route('/api/v1', methods=['GET'])
@cross_origin()
def get_dokumentation():
    json_obj = {
        "nodes":
            [
                {
                    "name": "name of node",
                    "address": "addess of the node",
                    "type": "address of the node type",
                    "attributes": [
                        {
                            "name": "Name of the attribute",
                            "dataType": "type of the attribute (supports int, number, string)",
                            "value": "value of the attribute"
                        }
                    ]
                }
            ],
        "links": [
            {
                "subject": "address of the subject",
                "predicate": "predicate address",
                "object": "object address"
            }
        ],
        "namespace": "the namespace of the model"
    }
    return "<h1>Privacy risk anslyses</h1> <p>Use endpoint POST /api/v1</p> <p> JSON object to pass:<p/><p>" + json.dumps(
        json_obj, indent=4, sort_keys=True) + "</p>"


@cross_origin()
@app.route('/api/v1', methods=['POST'])
@cross_origin()
def run_analyses():
    json_obj = request.json
    if "nodes" in json_obj and "links" in json_obj and "namespace" in json_obj:
        response = jsonify(execute_template.run_analyses(json_obj))
        return response
    else:
        return "Error"


@cross_origin()
@app.route('/echo', methods=['POST'])
def hello():
    return jsonify(request.json)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
