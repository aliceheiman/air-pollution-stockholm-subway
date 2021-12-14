"""
helperfunctions.py

General functions for Stockholm Air Pollution project.
"""

################################
# LIBRARIES
################################
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import dates
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

################################
# OS FUNCTIONS
################################


def get_folder_paths(folder_name):
    """Returns a of paths to sub-folders in parent folder."""

    # Get all sub-folders in parent folder
    folders = [f for f in os.listdir(folder_name) if os.path.isdir(f"{folder_name}/{f}")]

    # Append sub-folder name to parent folder to construct file path
    folders = [f"{folder_name}/{f}" for f in folders]

    return folders


################################
# FUNCTIONS
################################

################################
# FILTER FUNCTIONS
################################

# HELPER FUNCTIONS
def get_dataframe(sensor, filename):
    return pd.read_csv(f"./input/Sensor {sensor}/{filename}", skiprows=1, usecols=["Date", "Time"])


def get_time_label(timestamp):
    timestamp = timestamp + 20000

    if 0 < timestamp < (120000):
        return "AM"  # before lunch
    if 120000 <= timestamp < 240000:
        return "PM"  # after lunch


def get_date_label(date):
    date = str(date)

    return date[:4] + "-" + date[4:6] + "-" + date[6:]


def get_middle_value(df, column):
    """Sorts a dataframe by column name and returns the middle row."""

    # Sort dataframe by column
    t_df = df.sort_values(by=[column])

    # Pick out column value in middle
    n = int(len(t_df) / 2)

    # Get the middle record
    row = df.iloc[n]

    return row[column]


def get_green_line():
    """Returns the green line in the correct order."""

    green_line = [
        "Islandstorget",
        "Angbyplan",
        "Åkeshov",
        "Brommaplan",
        "Abrahamsberg",
        "Stora mossen",
        "Alvik",
        "Kristineberg",
        "Thorildsplan",
        "Fridhemsplan",
        "St Eriksplan",
        "Odenplan",
        "Rådmansgatan",
        "Hötorget",
        "T-Centralen",
        "Gamla Stan",
        "Slussen",
        "Medborgarplatsen",
        "Skanstull",
        "Gullmarsplan",
    ]

    return green_line


def get_sessions_by_column(df, column, value):
    """Returns all rows in dataframe where a column has the specified value."""
    return df.loc[df[column] == value]


def sort_by_green_line(x_list, y_list):
    """Returns a list of stations and their values in the correct order, as sorted by the green line."""

    # Get green line array
    green_line = get_green_line()

    # Store indexes of stations
    indexes = {}

    # Go through stations and their corresponding values
    for x, y in zip(x_list, y_list):
        try:
            # Locate station on green line
            i = green_line.index(x)
            if i not in indexes:
                indexes[i] = []

            # Store information with correct index
            indexes[i].append((x, y))
        except:
            continue

    # Create a new sorted list
    sorted_line = []

    # Go through every station on green line
    for i in range(len(green_line)):
        # If data for station
        if i in indexes:
            # Add all data for that station
            for pair in indexes[i]:
                sorted_line.append(pair)

    # Extract stations and values into separate arrays
    sorted_x = [s[0] for s in sorted_line]
    sorted_y = [s[1] for s in sorted_line]

    # Return storted data
    return sorted_x, sorted_y
