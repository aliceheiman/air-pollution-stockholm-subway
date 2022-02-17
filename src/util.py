"""
helperfunctions.py

General functions for Stockholm Air Pollution project.
"""

################################
# LIBRARIES
################################
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


def create_folder(folder_name):
    """Creates a folder if it does not exist and returns the folder name."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    return folder_name


################################
# TIME FUNCTIONS
################################


def get_time(timestr):
    return datetime.strptime(timestr, "%H:%M:%S").time()


def get_timestamp(timestr, date, offset=0):
    """Converts a string into a datetime object, adding

    Args:
        timestr (str): Time in format H:M:S
        date (str): Current date in format Y-m-d
        offset (int, optional): How many seconds to offset the original timestr. Defaults to 0.

    Returns:
        datetime: Datetime object from timestr and date with the added offset.
    """
    return datetime.strptime(f"{date} {timestr}", "%Y-%m-%d %H:%M:%S") + timedelta(seconds=offset)


def add_secs(initial, secs):
    """Adds x amount of seconds to a timestamp."""
    return initial + timedelta(seconds=secs)


def format_time(date, time_int):
    # convert int to str
    str_time = str(time_int)

    # Pad 5:00:00 to 05:00:00
    if len(str_time) < 6:
        str_time = "0" + str_time

    # Concatenate date and time
    str_time = date + " " + str_time

    # Convert string into date time object
    result = datetime.strptime(str_time, "%Y-%m-%d %H%M%S")

    return result


################################
# OTHER FUNCTIONS
################################

# Morning and evening
def morning(x):
    return (x >= "06:00:00") & (x <= "09:00:00")


def evening(x):
    return (x >= "15:00:00") & (x <= "18:00:00")


def get_middle_value(grp, column):
    # Sort dataframe by column
    t_df = grp.sort_values(by=[column])

    # Pick out column value in middle
    n = int(len(t_df) / 2)

    # Get the middle record
    row = t_df.iloc[n]

    # Return
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


def get_outside_stations():
    """Returns a list of outside stations."""

    outside_stations = [
        "Islandstorget",
        "Angbyplan",
        "Åkeshov",
        "Brommaplan",
        "Abrahamsberg",
        "Stora mossen",
        "Alvik",
        "Kristineberg",
        "Thorildsplan",
        "Gamla Stan",
        "Gullmarsplan",
    ]

    return outside_stations


def get_inside_stations():
    """Returns a list of inside stations."""

    green_line = [
        "Fridhemsplan",
        "St Eriksplan",
        "Odenplan",
        "Rådmansgatan",
        "Hötorget",
        "T-Centralen",
        "Slussen",
        "Medborgarplatsen",
        "Skanstull",
    ]

    return green_line
