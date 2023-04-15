# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 03:39:57 2023

@author: JoelT
"""
import pandas as pd


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

    for __, row in personatge_raw_data.iterrows():
        if row["isbn"] in personatge_formated_data:
            personatge_formated_data[row["isbn"]].append(
                {"_id": row["nom"], "tipus": row["tipus"]})
        else:
            personatge_formated_data[row["isbn"]] = [
                {"_id": row["nom"], "tipus": row["tipus"]}]

    return personatge_formated_data


def get_artistes(guionistes: str, dibuixants: str) -> dict:
    """


    Parameters
    ----------
    guionistes : str
        DESCRIPTION.
    dibuixants : str
        DESCRIPTION.

    Returns
    -------
    dict
        DESCRIPTION.

    """
    guionistes = guionistes[1:-1].split(", ")
    dibuixants = dibuixants[1:-1].split(", ")

    artistes = {}

    for guionista in guionistes:
        if guionista in artistes:
            artistes[guionista].append("guionista")
        else:
            artistes[guionista] = ["guionista"]

    for dibuixant in dibuixants:
        if dibuixant in artistes:
            artistes[dibuixant].append("dibuixant")
        else:
            artistes[dibuixant] = ["dibuixant"]

    return artistes
