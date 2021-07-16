# Face Verification Service
This is Face Verification endpoint to verify images from a Phone Selfie vs BVN

## Usage
All responses will have the form
```
{
    "Name": Name_of_customer,
    "distance": 0.424,
    "verify": boolean value(true/false)
}
```

Subsequent response definitions will only detail the expected value of the `data field`

**API Endpoints:**

* '/' :   return the facial verification documentation
* face_verification : return a Name, Distance, and Verification(true/false) for the bvn & selfie  images


# Installation
Install [face_recognition](https://github.com/ageitgey/face_recognition) together with [dlib](http://dlib.net/) first.
Then run: pip install -r requirements.txt


## Definition

`Get/face_verification`
## Response
* `200 OK` on success

```
{
    "message": "endpoint is working",
    "status": "success"
}
```

# Getting a Face verified
## Definition
`POST / face_verification`

### Arguments
* url to bvn image
* url to selfie image

## Response
* `201 Created on success`

```
{
    "identifier": "floor-lamp",
    "name": "Floor Lamp",
    "device_type": "switch",
    "controller_gateway": "192.1.68.0.2"
}
```

# How to Run
## Prerequisites
Prepare some known faces as a database for face_rec API in sample_images folder, and modify known_faces in face_util.py accordingly.
```
# Each face is tuple of (Name,sample image)    
known_faces = [('Obama','sample_images/obama.jpg'), 
               ('Peter','sample_images/peter.jpg'),
              ]
```
## Run API Server
python flask_server.py


## Run API client - Web
Simply open a web browser and enter:

http://127.0.0.1:5001/face_rec

http://127.0.0.1:5001/face_match

and upload image files.

## Run API client - Python
python demo_client.py 


