from flask import Flask, request, jsonify,send_file
from flask_cors import CORS
import pandas
from flask_pymongo import PyMongo
import ast
import datetime
import os
import csv

app = Flask(__name__)
CORS(app)

mongodb_client = PyMongo(
    app, uri="mongodb+srv://vysh:vysh@cluster0.riwdt.mongodb.net/flask?retryWrites=true&w=majority")
db = mongodb_client.db


@app.route("/data",  methods=['GET', 'POST'])
def handle_file():
    if request.method == "POST":
        file = request.files['file']
        df = pandas.read_csv(file)
        data1 = df["image_name"]
        data2 = df["objects_detected"]
        data3 = df["timestamp"]

        n = len(data1)
        for i in range(n):
            db.csv.insert_one(
                {'image_name': data1[i], 'objects_detected': data2[i], 'timestamp': data3[i]})

        return jsonify({
            "status": "success",
            "message": "111"
        }), 200, {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        }
    elif request.method == "GET":
        key = str(request.query_string).split("=")[1][:-1]
        file = os.path.join("images", key)
        print(file)
        return send_file(file), 200, {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        }


@app.route("/date",  methods=['GET', 'POST'])
def handle_date():
    if request.method == "POST":
        sd = ast.literal_eval(request.data.decode("UTF-8"))["sd"]
        ed = ast.literal_eval(request.data.decode("UTF-8"))["ed"]

        sd = list(map(lambda x: int(x), sd.split("-")))
        ed = list(map(lambda x: int(x), ed.split("-")))
        print(sd, ed)
        d1 = datetime.datetime(sd[0], sd[1], sd[2])
        d2 = datetime.datetime(ed[0], ed[1], ed[2])

        data = db.csv.find()
        response = []
        for e in data:
            nd = list(map(lambda x: int(x), e["timestamp"].split("-")))
            d = datetime.datetime(nd[0], nd[1], nd[2])
            if d >= d1 and d <= d2:
                e["_id"] = str(e["_id"])
                response.append(e)
        
        dic = {}
        for d in response:
            arr = d["objects_detected"].split(",")
            for e in arr:
                if dic.get(e):
                    dic[e] += 1
                else:
                    dic[e] = 1
        

        with open('app/report.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            
            writer.writerow(["threat", "occurance"])
            for i in dic.keys():
                writer.writerow([i, dic[i]])

        return jsonify(response), 200, {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        }
