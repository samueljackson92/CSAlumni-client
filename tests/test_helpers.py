__author__ = "Samuel Jackson"
__date__ = "November 26, 2014"
__license__ = "MIT"

import os

FIXTURES_FOLDER = "fixtures"

def load_fixture(file_name):
    """Load a text file from the fixtures folder """
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, FIXTURES_FOLDER)
    file_name = os.path.join(path, file_name)
    with open(file_name, 'r') as file_handle:
        fixture_text = file_handle.read()
    return fixture_text
