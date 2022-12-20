#python3 -m flask run
from flask import Flask, request, jsonify
import os
import binascii
import markdown
from flask_cors import CORS
import logging
from authentication.auth import check_auth_header
from face_model import compare_face

LOG_FILENAME = "face-recognition.log"
logging.basicConfig(
    filename=LOG_FILENAME, level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S"
)

app = Flask(__name__)
CORS(app)
app.debug = True

ALLOWED_EXTENSIONS = ['data']

def allowed_file(url):
    return ';' in url and url.rsplit(':', 1)[0].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Represent some documention"""

    #Open the README file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:
        content = markdown_file.read()
        return markdown.markdown(content)


@app.route('/face_verification', methods=["GET"])
def home():
    return jsonify({"message": "endpoint is working", "status": "success"}), 200

@app.route('/face_verification', methods=['POST'])
def face_verify():
    validate_auth_header = check_auth_header()
    if not validate_auth_header[0]:
       return validate_auth_header[1]

    try:
        if request.method == 'POST':
            if request.is_json:
                # print('Request is a JSON format.')
                json_data = request.get_json(cache=False)
                # get('url1', None)
                url1 = json_data['NinImageUrl']
                #get('url2', None)
                url2 = json_data['selfieUrl']
                if not (allowed_file(url1)) or not (allowed_file(url2)):
                    return { 'status' : None,
                            'distance': None,
                            'message':  "Invalid JSON File"
                
                        }, 400

                if allowed_file(url1) and allowed_file(url2):
                    verify = compare_face(url1, url2)
                
                return jsonify(verify)
    except (binascii.Error,TypeError) as e:
        print('Invalid base64-encoded string', e)
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)