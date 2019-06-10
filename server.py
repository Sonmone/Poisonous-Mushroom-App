from flask import Flask, request, Response
#from mushroom.model.tools.predict import predict
#import jsonpickle
import numpy as np
import cv2
import datetime
import base64
import json

#import predict model
import sys
sys.path.append('/root/mushroom/tf-faster-rcnn/tools')
from predict import Predict
predictor = Predict()



# Initialize the Flask application
app = Flask(__name__)
@app.route('/')
def connect():
    response = {'from':'35.201.9.84','connection':'true','timestamp':str(datetime.datetime.now())}
    response_json = json.dumps(response)
    return response_json



@app.route('/hello')
def hello():
    return 'Hello World!'


# route http posts to this method
@app.route('/predict', methods=['POST'])
def test():
    print("received the request")
    r = request
    received_data = base64.b64decode(r.data)
    image = 'data/' + str(datetime.datetime.now())+'.jpg'
    f = open(image,'wb')
    f.write(received_data)
    f.close()
    img = cv2.imread(image)
    print(img.shape)
    # Predict the image
    boxes = []
    className, classProb, boxes = predictor.predict(image)
    #print(type(boxes[0][0]))
  
    response = {'timestamp':str(datetime.datetime.now()),'className': className, 'classProb':classProb, 'boxes':boxes, 'info':'mushroom Information'}

    response_json = json.dumps(response)
    print(response_json) 
    return response_json   
   
# start flask app
print("Building the RCNN model...")
predictor.build_model()
print("Listening requests...")
app.run(host='0.0.0.0',port=80)
