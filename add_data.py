# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 03:37:26 2023

@author: JoelT
"""
import pymongo
import pandas as pd
from database_handler import get_collection
from get_data import get_artistes, get_characters


def add_data(database: pymongo.database.Database, file_name: str) -> None:
    """
    Adds to the database all data stored in the given file.
    Parameters
    ----------
    database : pymongo.database.Database
        pymongo database object containing the connection to the database.
    file_name : str
        Name of the file containing all the data to add to the database.
    Returns
    -------
    None
    """
    add_artists(database, file_name)
    add_editorials(database, file_name)
    add_publications(database, file_name)


def add_artists(database: pymongo.database.Database, file_name: str) -> None:
    """
    Adds all the artist in the given file to the "Artista" collection of the
    database.
    Parameters
    ----------
    database : pymongo.database.Database
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
    get_collection(database, "Artista").insert_many(artista_formated_data)


def add_editorials(database: pymongo.database.Database, file_name: str) -> None:
    """
    Adds all the editorial (and respective collections) in the given file to
    the "Editorial" collection of the database.

    Parameters
    ----------
    database : pymongo.database.Database
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
            {"_id": index[1], "total_exemplars": int(index[2]),
             "gèneres": index[3][1:-1].split(", "), "idioma": index[4],
             "any_inici": int(index[5]), "any_fi": int(index[6]),
             "tancada": index[7]})

    editorials_collecions_formated_data = list(
        editorials_collecions_raw_data.values())

    get_collection(database, "Editorial").insert_many(
        editorials_collecions_formated_data)


def add_publications(database: pymongo.database.Database, file_name: str) -> None:
    """
    Adds all the publications in the given file to the "Publicacio" collection
    of the database.

    Parameters
    ----------
    database : pymongo.database.Database
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
                                 "personatges":personatges_formated_data[row["ISBN"]],
                                 "artistes":get_artistes(row["guionistes"], row["dibuixants"])} if row["ISBN"] in personatges_formated_data else {"_id": row["ISBN"], "titol":row["titol"],
                                "autor":row["autor"],
                                "num_pàgines":row["num_pagines"],
                                "estoc":row["stock"], "preu":row["preu"],
                                "editorial":row["NomEditorial"],
                                "col·lecció":row["NomColleccio"],
                                "personatges": [], "artistes":get_artistes(row["guionistes"], row["dibuixants"])} for index, row in colleccions_publicacions_raw_data.iterrows()]

    get_collection(database, "Publicacio").insert_many(
        publicacio_formated_data)
