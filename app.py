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

predi = kmeanModel.predict(data_set)
data_set2 = data_set
data_set2['k-means'] = predi


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

@app.route('/media', methods=['GET'])
def media():

    k_means_0 = data_set['k-means']  == 0
    k_means_1 = data_set['k-means']  == 1
    k_means_2 = data_set['k-means']  == 2

    data0 = data_set[k_means_0]
    data1 = data_set[k_means_1]
    data2 = data_set[k_means_2]

    prom0 = [
        data0['Grams'].mean(),
        data0['Calories'].mean(),
        data0['Protein'].mean(),
        data0['Fat'].mean(),
        data0['Sat.Fat'].mean(),
        data0['Fiber'].mean(),
        data0['Carbs'].mean()
    ]

    prom1 = [
        data1['Grams'].mean(),
        data1['Calories'].mean(),
        data1['Protein'].mean(),
        data1['Fat'].mean(),
        data1['Sat.Fat'].mean(),
        data1['Fiber'].mean(),
        data1['Carbs'].mean()
    ]

    prom2 = [
        data2['Grams'].mean(),
        data2['Calories'].mean(),
        data2['Protein'].mean(),
        data2['Fat'].mean(),
        data2['Sat.Fat'].mean(),
        data2['Fiber'].mean(),
        data2['Carbs'].mean()
    ]
    
            
    return jsonify({"status": "ok","promedios":[prom0, prom1, prom2]})

if __name__ == "__main__":
    app.run()