from flask import Flask, request, render_template
import requests
from torchvision import transforms
import torch
import re
from PIL import Image
from io import BytesIO
import numpy as np
import pickle

app = Flask(__name__)

# Load the pre-trained model 

model = torch.load('mobnet_model.pth', map_location ='cpu')

def predict_one(model, inputs):
    with torch.no_grad():
        model.eval()
        logit = model(inputs).cpu()
        probs = torch.nn.functional.softmax(logit, dim=-1).numpy()
    return probs

img_size = 224

def get_image(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    image.load()
    image = image.convert('RGB').resize((img_size, img_size))
    preprocess = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
    X = np.array(image)
    X = np.array(X / 255, dtype='float32')
    X = preprocess(X) 
    return X


# Define the prediction endpoint

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict', methods=['POST'])
def predict():
    img_url = request.form.get("peng")
    img = get_image(img_url)
    label_encoder = pickle.load(open("label_encoder.pkl", 'rb'))
    prob = predict_one(model, img.unsqueeze(0))
    predict_proba = np.max(prob)*100
    predicted_species = label_encoder.classes_[np.argmax(prob)]
    results = "Prediction: {} with confidence {:.0f}%".format(predicted_species,predict_proba)
    return render_template('result.html', results = results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

