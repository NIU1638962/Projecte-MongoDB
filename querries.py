# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 12:52:38 2023

@author: JoelT
"""
import pprint
from database_handler import connect_database, get_collection

db = connect_database("test")

colleccio_Publicacions = get_collection(db, "Publicacio", False)

colleccio_Editorials = get_collection(db, "Editorial", False)

# -----------------------------------------------------------------------------------------
# 1.
result_1 = list(colleccio_Publicacions.aggregate([{"$project": {"_id": 0, "titol": 1, "preu": 1}},
                                                  {"$sort": {"preu": -1}},
                                                  {"$limit": 5}]))
print("-".join(["-" for i in range(45)]) + str("\n1: "))
pprint.pprint(result_1)

# -----------------------------------------------------------------------------------------
# 2.
result_2 = list(colleccio_Publicacions.aggregate([
    {"$match": {"editorial": "Juniper Books"}},
    {"$group": {
        "_id": "$editorial",
        "minim": {"$min": "$preu"},
        "maxim": {"$max": "$preu"},
        "avg": {"$avg": "$preu"},
    }},
    {"$project": {"_id": 0}}
]))

print("-".join(["-" for i in range(45)]) + str("\n2: "))
pprint.pprint(result_2)

# -----------------------------------------------------------------------------------------
# 3.
result_3 = list(colleccio_Publicacions.aggregate([
    {"$project": {"artistes.dibuixants": 1}},
    {"$unwind": "$artistes.dibuixants"},
    {"$group": {"_id": "$artistes.dibuixants",
                "aparicions": {"$count": {}}}},
    {"$match": {"aparicions": {"$gt": 5}}},
    {"$project": {"_id": 0, "nom_artístic": "$_id"}},
    {"$sort": {"aparicions": 1}}
]))

print("-".join(["-" for i in range(45)]) + str("\n3: "))
pprint.pprint(result_3)

# -----------------------------------------------------------------------------------------
# 4.
result_4 = list(colleccio_Editorials.aggregate([
    {"$unwind": "$col·leccions"},
    {"$unwind": "$col·leccions.gèneres"},
    {"$group": {
        "_id": "$col·leccions.gèneres",
        "num_coll": {"$sum": 1}
    }},
    {"$project": {"genere": "$_id", "_id": 0, "num_coll": 1}},
    {"$sort": {"num_coll": -1}}
])
)

print("-".join(["-" for i in range(45)]) + str("\n4: "))
pprint.pprint(result_4)

# -----------------------------------------------------------------------------------------
# 5.
result_5 = list(colleccio_Editorials.aggregate([
    {"$unwind": "$col·leccions"},
    {"$unwind": "$col·leccions.tancada"},
    {"$group": {
        "_id": "$_id",
        "final": {"$sum": {"$cond": [{"$eq": ["$col·leccions.tancada", True]}, 1, 0]}},
        "nofinal": {"$sum": {"$cond": [{"$eq": ["$col·leccions.tancada", False]}, 1, 0]}}}}
])
)
print("-".join(["-" for i in range(45)]) + str("\n5: "))
pprint.pprint(result_5)

# -----------------------------------------------------------------------------------------
# 6.
result_6 = list(colleccio_Editorials.aggregate([
    {"$unwind": "$col·leccions"},
    {"$match": {"col·leccions.tancada": True}},
    {"$sort": {"col·leccions.total_exemplars": -1}},
    {"$limit": 2},
    {"$project": {"_id": 0, "editorial": "$_id", "coll": "$col·leccions._id"}}
]))

print("-".join(["-" for i in range(45)]) + str("\n6: "))
pprint.pprint(result_6)

# -----------------------------------------------------------------------------------------
# 7.
result_7 = list(colleccio_Publicacions.aggregate([
    {"$unwind": "$artistes.guionistes"},
    {"$group": {
        "_id": "$artistes.guionistes",
        "num_guiones": {"$count": {}}
    }},
    {"$sort": {"num_guiones": -1}},
    {"$limit": 1},  # Este numero se puede cambiar
    {"$lookup": {
        "from": "Artista",
        "localField": "_id",
        "foreignField": "_id",
        "as": "datos_artista"
    }},
    {"$project": {"_id": 0, "pais": "$datos_artista.pais"}}
]))

print("-".join(["-" for i in range(45)]) + str("\n7: "))
pprint.pprint(result_7)

# -----------------------------------------------------------------------------------------
# 8.
result_8 = list(colleccio_Publicacions.aggregate(
    [{"$unwind": "$personatges"},
     {"$group": {"_id": "$_id", "tipus": {"$addToSet": "$personatges.tipus"}}},
     {"$match": {"$and": [{"tipus": {"$size": 1}},
                          {"tipus.0": "heroe"}]}},
     {"$project": {"ISBN": "$_id", "_id": 0}}]))

print("-".join(["-" for i in range(45)]) + str("\n8: "))
pprint.pprint(result_8)

# -----------------------------------------------------------------------------------------
# 9.
result_9_pre = list(colleccio_Publicacions.find(
    {"estoc": {"$gte": 20}}, projection={"_id": 1, "preu": 1}))

colleccio_Publicacions.update_many(
    {"estoc": {"$gte": 20}},
    {"$mul": {"preu": 1.25}}
)

result_9_aft = list(colleccio_Publicacions.find(
    {"estoc": {"$gte": 20}}, projection={"_id": 1, "preu": 1}))


print("-".join(["-" for i in range(45)]) + str("\n9: "))
pprint.pprint(result_9_pre)
print("\n")
pprint.pprint(result_9_aft)

# -----------------------------------------------------------------------------------------
# 10.
result_10 = list(colleccio_Publicacions.aggregate([
    {
        "$project": {
            "_id": 0,
            "ISBN": "$_id",
            "titol": 1,
            "personatges": 1
        }
    }
]))

print("-".join(["-" for i in range(45)]) + str("\n10: "))
pprint.pprint(result_10)

# -----------------------------------------------------------------------------------------
print("-".join(["-" for i in range(45)]))
