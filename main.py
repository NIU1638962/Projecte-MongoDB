# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 10:47:53 2023

@author: JoelT
"""
import pymongo
import pandas as pd
from options import Options


def connect_database(database_name: str, local_test: bool = False) -> pymongo.database.Database:
    """
    Connects to the database and returns the pymongo object.

    Parameters
    ----------
    database_name : str
        Name of the database.
    local_test : bool, optional
        If true connects to the local database instead of the server. The default is False.

    Returns
    -------
    pymongo.database.Database
        pymongo database object.

    """
    if local_test:
        dsn = "mongodb://{}:{}".format('localhost', 27017)
    else:
        dsn = "mongodb://{}:{}".format('dcccluster.uab.es', 8194)
    conn = pymongo.MongoClient(dsn)
    return conn[database_name]


def delete_database(db: pymongo.database.Database) -> None:
    """
    Deletes all documents and collections of the database.

    Parameters
    ----------
    db : pymongo.database.Database
        pymongo database object containing the connection to the database that
        wants to deleted.

    Returns
    -------
    None

    """
    for collection_name in db.list_collection_names():
        db.get_collection(collection_name).drop()


def get_collection(db: pymongo.database.Database, collection_name: str) -> pymongo.collection.Collection:
    """
    Get and return the pymongo collection object given a database, if doesn't
    exist creates it and if exists deletes all documents on it.

    Parameters
    ----------
    db : pymongo.database.Database
        pymongo database object containing the connection to the database.
    collection_name : str
        Name of the collection we want to obtain the object off.

    Returns
    -------
    pymongo.collection.Collection
        pymongo collection object containing the connection to the database collection.

    """
    try:
        collection = db.create_collection(collection_name)
    except pymongo.errors.CollectionInvalid:
        collection = db.get_collection(collection_name)
        collection.drop()
    return collection


def add_data(db: pymongo.database.Database, file_name: str) -> None:
    """
    Adds to the database all data stored in the given file.

    Parameters
    ----------
    db : pymongo.database.Database
        pymongo database object containing the connection to the database.
    file_name : str
        Name of the file containing all the data to add to the database.

    Returns
    -------
    None

    """
    add_artists(db, file_name)


def add_artists(db: pymongo.database.Database, file_name: str) -> None:
    """
    Adds all the artist in the given file to the "Artista" collection of the
    database.

    Parameters
    ----------
    db : pymongo.database.Database
        pymongo database object containing the connection to the database.
    file_name : str
        Name of the file containing all the data to add to the database.

    Returns
    -------
    None

    """
    artista_raw_data = pd.read_excel(file_name, "Artistes")
    artista_formated_data = [{"_id": row["Nom_artistic"], "nom": row["nom"],
                              "cognoms": row["cognoms"],
                              "data_naixement": row["data_naix"],
                              "pais": row["pais"]} for index, row in artista_raw_data.iterrows()]
    get_collection(db, "Artista").insert_many(artista_formated_data)


if __name__ == "__main__":
    arguments = Options().parse()
    db = connect_database(arguments.db, local_test=True)
    if arguments.delete_all:
        delete_database(db)
    elif arguments.fileName:
        add_data(db, arguments.fileName)
