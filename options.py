# -*- coding: utf-8 -*-
"""
    Parse input arguments

    Original author:
        __author__ = 'Oriol Ramos Terrades'
        __email__ = 'oriolrt@cvc.uab.cat'

"""


from argparse import ArgumentParser, HelpFormatter
from operator import attrgetter


class SortingHelpFormatter(HelpFormatter):

    def add_arguments(self, actions):
        actions = sorted(actions, key=attrgetter('option_strings'))
        super(SortingHelpFormatter, self).add_arguments(actions)


class Options(ArgumentParser):

    def __init__(self):
        # MODEL SETTINGS
        super().__init__(description="This script inserts data into a mongo-powered database that stores book information",
                         formatter_class=SortingHelpFormatter)
        # Positional arguments
        super().add_argument('-f', '--fileName', type=str,
                             help='EXCEL File where data is stored.')
        super().add_argument('--db', type=str, required=True,
                             help='Select the database to perform the operations')
        # Optional arguments
        super().add_argument('--delete-all',
                             help='Delete all files from the selected DB.', action="store_true")

    def parse(self):
        return super().parse_args()
