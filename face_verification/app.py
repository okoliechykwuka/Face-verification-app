#python3 -m flask run
from flask import Flask, request, redirect, jsonify
import os
import markdown
from flask_cors import CORS
import logging
import numpy as np
import cv2
import imutils
import urllib
from skimage import io 
import re
import urllib
from authentication.auth import check_auth_header
from face_model import compare_face, get_selfie_encoding, get_bvn_encoding

LOG_FILENAME = "face-recognition.log"
logging.basicConfig(
    filename=LOG_FILENAME, level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S"
)

app = Flask(__name__)
CORS(app)
app.debug = True

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

def read_selfie_url(url):
    # pattern = pattern = re.compile(r'(?<=_)[a-z_]+(?=_)', re.IGNORECASE)
    # sequence = url
    # name = pattern.search(sequence).group()
    img = io.imread(url)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    bgr_image = imutils.resize(img, width=500)
    return bgr_image #name

def read_bvn_url(url):
    img = io.imread(url)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    bgr_image = imutils.resize(img, width=500)
    return bgr_image

def allowed_file(url):
    return '.' in url and url.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS

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

    # verify = None
    # try:
    if request.method == 'POST':
        if request.is_json:
            # print('Request is a JSON format.')
            json_data = request.get_json(cache=False)
            # get('url1', None)
            url1 = json_data['bvnImageUrl']
            #get('url2', None)
            url2 = json_data['selfieUrl']
            
            if not (allowed_file(url1)) or not (allowed_file(url2)):
                return { 'status' : None,
                        'distance': None,
                        'message':  "Invalid JSON File"
              
                      }, 400

            if allowed_file(url1) and allowed_file(url2):
                bvnImageUrl = read_bvn_url(url1)
                selfieUrl = read_selfie_url(url2)
                selfie_image = get_selfie_encoding(selfieUrl)
                bvn_image =  get_bvn_encoding(bvnImageUrl)

                verify = compare_face(selfie_image, bvn_image)
# except urllib.error.HTTPError as  error:
    #     print(error)

            return jsonify(verify)
    



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)