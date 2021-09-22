from pymongo import MongoClient
import time
import pandas as pd
import json

files=["1K","100K","1M","3M","10M","historical_stock_prices"]

client = MongoClient("mongodb://10.27.0.20:27017/")

with open("Result_query/report_mongo_cluster.txt","a") as report:
  for f in files:
    for n in client.list_databases():
        if "test"==n["name"]:
            client.drop_database("test")
    database = client['test']
    mycol = database['hsp']
    start_query = time.time()
    print("init query {}".format(start_query))
    data = pd.read_csv('dataset/'+f+'.csv')
    payload = json.loads(data.to_json(orient='records'))
    mycol.insert_many(payload)
    min_data = mycol.aggregate([{"$group": {"_id": "$ticker", "data_min": {"$min": "$date"}}}])
    d_min_data = {}
    for d in min_data:
        d_min_data[d["_id"]] = d["data_min"]

    max_data = mycol.aggregate([{"$group": {"_id": "$ticker", "data_max": {"$max": "$date"}}}])
    d_max_data = {}
    for d in max_data:
        d_max_data[d["_id"]] = d["data_max"]

    min_price = mycol.aggregate([{"$group": {"_id": "$ticker", "min_price": {"$min": "$low"}}}])
    d_min_price = {}
    for d in min_price:
        d_min_price[d["_id"]] = d["min_price"]

    max_price = mycol.aggregate([{"$group": {"_id": "$ticker", "max_price": {"$max": "$high"}}}])
    d_max_price = {}
    for d in max_price:
        d_max_price[d["_id"]] = d["max_price"]
    end = time.time()

    d = {}
    for k in d_min_data.keys():
        xi_cursor = mycol.find({"$and": [{"ticker": k}, {"date": d_min_data.get(k)}]})
        for i in xi_cursor:
            xi = i["close"]
        xf_cursor = mycol.find({"$and": [{"ticker": k}, {"date": d_max_data.get(k)}]})
        for i in xf_cursor:
            xf = i["close"]

        d[k] = [d_min_data.get(k), d_max_data.get(k), d_min_price.get(k), d_max_price.get(k), ((xf - xi) / xi) * 100]

    end_query = time.time()
    query_time = end_query - start_query
    print("query({}) eseguita in {}\n".format(f,query_time))
    report.write("{}\t{}\n{}\n\n".format(f,query_time,d))