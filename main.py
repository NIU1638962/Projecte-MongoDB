# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 10:47:53 2023

@author: JoelT
"""
from sys import argv
from pymongo import MongoClient
import pandas

try:
    file = argv[1]

    DSN = "mongodb://{}:{}".format('dcccluster.uab.es', 8194)
    conn = MongoClient(DSN)
    bd = conn['Projecte']
    try:
        coll = bd.create_collection("MongoDB")
    except:
        coll = bd["MongoDB"]
    coll.drop()

    transactions = pandas.read_csv(file)
    coll.insert_many(transactions.to_dict("records"))

except IndexError:
    print("Error: No s'ha passat argument.")
