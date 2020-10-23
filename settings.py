# settings.py

"""Module for app constants as database name and images path"""

import os
import sys

# Database file name
DATABASE = 'sqlite:///teamplayers.db?check_same_thread=False'

# Images path
platform = sys.platform

IMG_PATH = os.getcwd() + "//images//" if "linux" in platform.lower() \
        else os.getcwd() + "\\images\\"

IMPORT_PATH = os.getcwd() + '//days//' if "linux" in platform.lower() \
              else os.getcwd() + '\\days\\'

# Fantacalcio rules

BUDGET = 500
TRADES = 5
GOALKEEPER = 3
DEFENDERS = 8
MIDFIELDERS = 8
FORWARDS = 6

