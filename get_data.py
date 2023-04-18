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
        sring of shape "[artist1, artista2, ...]" with the artsits id's of
        those that were writers.
    dibuixants : str
        sring of shape "[artist1, artista2, ...]" with the artsits id's of
        those that were drawers.

    Returns
    -------
    dict
        dictionary of lists, with roles as keys and then a list of the artists
        id's of that role.

    """

    return {
        "guionistes": guionistes[1:-1].split(", "),
        "dibuixants": dibuixants[1:-1].split(", ")}
