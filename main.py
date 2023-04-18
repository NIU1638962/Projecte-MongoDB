# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 10:47:53 2023
@author: JoelT
"""
from options import Options
from add_data import add_data
from database_handler import connect_database, delete_database


if __name__ == "__main__":
    arguments = Options().parse()
    db = connect_database(arguments.db)
    if arguments.delete_all:
        delete_database(db)
    elif arguments.fileName:
        add_data(db, arguments.fileName)
