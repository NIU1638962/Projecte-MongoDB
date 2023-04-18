# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 03:35:06 2023

@author: JoelT
"""
from pymongo import collection, database, errors, MongoClient


def connect_database(database_name: str, local_test: bool = False) -> database.Database:
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
        host = 'localhost'
        port = 27017
    else:
        host = 'dcccluster.uab.es'
        port = 8194
    dsn = f"mongodb://{host}:{port}"
    conn = MongoClient(dsn)
    return conn[database_name]


def delete_database(db_conn: database.Database) -> None:
    """
    Deletes all documents and collections of the database.
    Parameters
    ----------
    db_conn : pymongo.database.Database
        pymongo database object containing the connection to the database that
        wants to deleted.
    Returns
    -------
    None
    """
    for collection_name in db_conn.list_collection_names():
        db_conn.get_collection(collection_name).drop()


def get_collection(db_conn: database.Database, collection_name: str,
                   drop: bool = False) -> collection.Collection:
    """
    Get and return the pymongo collection object given a database, if doesn't
    exist creates it and if exists deletes all documents on it.
    Parameters
    ----------
    db_conn : pymongo.database.Database
        pymongo database object containing the connection to the database.
    collection_name : str
        Name of the collection we want to obtain the object off.
    drop : bool
        If the collection already exist, true drops it, false doesn't.
    Returns
    -------
    pymongo.collection.Collection
        pymongo collection object containing the connection to the database collection.
    """
    try:
        collection_reference = db_conn.create_collection(collection_name)
    except errors.CollectionInvalid:
        collection_reference = db_conn.get_collection(collection_name)
        if drop:
            collection_reference.drop()
    return collection_reference
