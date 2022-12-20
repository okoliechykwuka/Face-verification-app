# import face_recognition as fr
# import os
# import cv2
# import numpy as np
# import imutils
# import re
# from skimage import io


# TOLERANCE = 0.49
# MODEL = 'cnn'  # default: 'hog', other one can be 'cnn' - CUDA accelerated (if available) deep-learning pretrained model

# # get captured face encodings and names
# def get_selfie_encoding(image):

#     locations = fr.face_locations(image, model=MODEL)
#     if len(locations) == 0:
#         return []
#     try:
#         camera_encoding = fr.face_encodings(image, locations)[0]
#     except IndexError:
#         print('The face was not captured rightly, retake the image') 

#     return camera_encoding
# # known_names, selfie_face_encoding = get_selfie_encoding('test_images/simon.jpg')
# # print(camera_face_encoding)

# def get_bvn_encoding(image):
#     # Load image
#     # print(f'Filename {filename}', end='')

#     # This time we first grab face locations - we'll need them to draw boxes
#     locations = fr.face_locations(image, model=MODEL)

#     # # Now since we know loctions, we can pass them to face_encodings as second argument
#     # # Without that it will search for faces once again slowing down whole process
#     encodings = fr.face_encodings(image, locations)[0]
#     # # We passed our image through face_locations and face_encodings, so we can modify it
#     # # First we need to convert it from RGB to BGR as we are going to work with cv2
#     return encodings
# # bvn_encoding = get_bvn_encoding('test_images/akon_15.jpeg')

# def compare_face(camera_encoding, bvn_encoding):

#     if len(camera_encoding) == 0 or len(bvn_encoding) == 0:
#         return { 'status' : None,
#                         'distance': None,
#                         'message':  'Retake selfie image'
              
#                       }
        
       
   
    
#     results = fr.compare_faces([camera_encoding], bvn_encoding, TOLERANCE)
#     distance = fr.api.face_distance([camera_encoding], bvn_encoding).tolist() 
#     image_distance = round(distance[0],3)
#     verification = { 'status' : bool(results[0]),
#                         'distance': image_distance,
#                         'message': 'verified successfully'
#                       }

#     return verification


# verification = compare_face(selfie_face_encoding, bvn_encoding)
# print(verification)

from PIL import Image
import base64
import numpy
from io import BytesIO
import cv2
import face_recognition
import time
TOLERANCE = 0.5

def decode_image(base64_image):
    encoded_image = base64_image.split(",")[1]
    decoded_image = base64.b64decode(encoded_image)
    img = Image.open(BytesIO(decoded_image))#.convert('LA')
    pixels = numpy.asarray(img, dtype='uint8')
    resized_image = cv2.resize(pixels, (0, 0), fx=0.25, fy=0.25)
    encodings = face_recognition.face_encodings(resized_image)[0]

    return encodings

def compare_face(camera_byte, nin_byte):
    start_time = time.time()
    camera_image = decode_image(camera_byte)
    nin_image = decode_image(nin_byte)
    print(nin_image.shape)
    results = face_recognition.compare_faces([camera_image], nin_image,TOLERANCE)
    if len(camera_image) == 0 or len(nin_image) == 0:
        print("--- %s seconds ---" % (time.time() - start_time))
        return { 'status' : None,
                        'distance': None,
                        'message':  'Retake selfie image'
                      }
    else:
        distance = face_recognition.api.face_distance([camera_image], nin_image).tolist() 
        image_distance = round(distance[0],3)
        print("--- %s seconds ---" % (time.time() - start_time))
        return { 'status' : bool(results[0]),
                            'distance': image_distance,
                            'message': 'verified successfully'
                        }








