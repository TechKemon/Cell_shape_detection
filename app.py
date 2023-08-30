import pickle

from flask import Flask, request

app = Flask(__name__)

model_pickle = open("./Achira.pkl", "rb")
clf = pickle.load(model_pickle)

@app.route("/ping", methods=['GET'])
def ping():
    return {"message": "Hi there, I'm working with the new API. Can you kindly input the parameters needed to run my model!!"}

@app.route("/params", methods=['GET'])
def get_application_params():
    """
    """
    parameters = {
    'input_path': "<path>",
    'Dimensions': "<1024/512>",
    'Number_of_Images': "100/1000",
    'Shapes_to_detect': "4",
    'Shapes_to_Draw': "<10/20>"
    }
    return parameters

##defining the endpoint which will make the prediction
@app.route("/classify", methods=['POST'])
def classify():
    """
    Returns bounding boxes along with its class
    """
    req = request.get_json()
    print(req)

    if req['Dimensions'] == "1024":
        M = 1024
    else:
        M = 512
    
    if req['Number_of_Images'] == "100":
        num = 100
    else:
        num = 1000
 
    if req['Shapes_to_Draw'] == "10":
        N = 10
    else:
        N = 20
    
    input_path = req['input_path']
    Shapes_to_detect = req['4']

    result = clf.classify([[input_path, Dimensions, Number_of_Images, Shapes_to_detect, Shapes_to_Draw]])

    if result >= 0.90:
        pred = "Good Accuracy"
    else:
        pred = "More Improvement needed"
    
    return {"Final_detection_status": pred}