from flask import Flask
from flask import request
from flask import jsonify 
from flask_cors import CORS

import csv
import pandas as pd
import numpy as np
import re

from sklearn.cluster import KMeans
from sklearn import datasets

app = Flask(__name__)
CORS(app)

with open('nutrients_csvfile.csv', newline='') as File:  
    reader = pd.read_csv(File)
data_set = pd.DataFrame(reader)
data_set = reader.drop(["Food"], axis=1)
data_set = data_set.drop(["Category"], axis=1)
data_set = data_set.drop(['Measure'], axis=1)
data_set = data_set.replace("t", 0.2)
data_set = data_set.replace("t'", 0.2)
data_set = data_set.replace("a", 0)
data_set = data_set.astype(str)

for i in data_set:
    cont=0
    for j in data_set[i]:
        j = re.sub(",", "", j)
        j = re.sub("-","", j)
        j = re.sub("nan","0", j)
        data_set[i].values[cont] = j
        data_set[i].values[cont] = float(data_set[i].values[cont])
   
        cont+=1
print(data_set)

kmeanModel = KMeans(n_clusters=3)
kmeanModel.fit(data_set)

@app.route('/', methods=['POST'])
def index():

    #predi = kmeanModel.predict(data_set)

    produ = {
        "Grams": [request.json['Grams']],
        "Calories": [request.json['Calories']],
        "Protein": [request.json['Protein']],
        "Fat": [request.json['Fat']],
        "Sat.Fat": [request.json['Sat.Fat']],
        "Fiber": [request.json['Fiber']],
        "Carbs": [request.json['Carbs']],
    }
    
    product = pd.DataFrame(produ)
    print(product)
    prediccion = int(kmeanModel.predict(product))

    print(prediccion)
            
    return jsonify({"status": "ok","result": prediccion})

if __name__ == "__main__":
    app.run()