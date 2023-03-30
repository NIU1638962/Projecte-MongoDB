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
    add_editorials(db, file_name)
    add_publicacios(db, file_name)


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


def add_editorials(db: pymongo.database.Database, file_name: str) -> None:
    """
    Adds all the editorial (and respective collections) in the given file to
    the "Editorial" collection of the database.

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
    colleccions_publicacions_raw_data = pd.read_excel(
        file_name, "Colleccions-Publicacions")

    editorials_collecions_raw_data = {index[0]: {"_id": index[0],
                                                 "responsable": index[1],
                                                 "adreça": index[2],
                                                 "pais": index[3],
                                                 "col·leccions": []} for index, row in colleccions_publicacions_raw_data.groupby([
                                                     "NomEditorial",
                                                     "resposable",
                                                     "adreca",
                                                     "pais"]).count().iterrows()}

    for index, row in colleccions_publicacions_raw_data.groupby(["NomEditorial", "NomColleccio", "total_exemplars", "genere", "idioma", "any_inici", "any_fi", "tancada"]):
        editorials_collecions_raw_data[index[0]]["col·leccions"].append(
            {"_id": index[1], "total_exemplars": index[2],
             "gèneres": index[3][1:-1].split(", "), "idioma": index[4],
             "any_inici": int(index[5]), "any_fi": int(index[6]),
             "tancada": index[7]})

    editorials_collecions_formated_data = list(
        editorials_collecions_raw_data.values())

    get_collection(db, "Editorial").insert_many(
        editorials_collecions_formated_data)


def get_characters(file_name: str) -> dict:
    """
    Gets all the characters in the given file.
    Parameters
    ----------
    file_name : str
        Name of the file containing all the data to add to the database.
    Returns
    -------
    dict :
        Dictionaries with key ISBN and item a list of dictionaties where each
        dictionary is a character and their information.
    """
    personatge_raw_data = pd.read_excel(file_name, "Personatges")

    personatge_formated_data = {}

    for index, row in personatge_raw_data.iterrows():
        if row["isbn"] in personatge_formated_data.keys():
            personatge_formated_data[row["isbn"]].append(
                {"_id": row["nom"], "tipus": row["tipus"]})
        else:
            personatge_formated_data[row["isbn"]] = [
                {"_id": row["nom"], "tipus": row["tipus"]}]

    return personatge_formated_data


def add_publicacios(db: pymongo.database.Database, file_name: str) -> None:
    """
    Adds all the publications in the given file to the "Publicacio" collection
    of the database.

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
    colleccions_publicacions_raw_data = pd.read_excel(
        file_name, "Colleccions-Publicacions")

    personatges_formated_data = get_characters(file_name)

    publicacio_formated_data = [{"_id": row["ISBN"], "titol":row["titol"],
                                 "autor":row["autor"],
                                 "num_pàgines":row["num_pagines"],
                                 "estoc":row["stock"], "preu":row["preu"],
                                 "editorial":row["NomEditorial"],
                                 "col·lecció":row["NomColleccio"],
                                 "personatges":personatges_formated_data[row["ISBN"]]} for index, row in colleccions_publicacions_raw_data.iterrows()]

    get_collection(db, "Publicacio").insert_many(
        publicacio_formated_data)


if __name__ == "__main__":
    arguments = Options().parse()
    db = connect_database(arguments.db, local_test=True)
    if arguments.delete_all:
        delete_database(db)
    elif arguments.fileName:
        add_data(db, arguments.fileName)
