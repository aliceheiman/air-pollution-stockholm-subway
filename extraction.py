################################
# LIBRARIES
################################
import matplotlib.pyplot as plt
from matplotlib import dates
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

################################
# FUNCTIONS
################################


def get_middle_value(df, column):
    # Sort dataframe by column
    t_df = df.sort_values(by=[column])

    # Pick out column value in middle
    n = int(len(t_df) / 2)

    row = df.iloc[n]

    return row[column]


def algorithm_1_sessions():
    """
    Goes through all sessions and takes the median value for every station record.
    """

    # Save all sessions in array
    sessions = []

    # Get all date folders
    folders = [f for f in os.listdir("sessions") if os.path.isdir(f"sessions/{f}")]
    folders = [f"sessions/{f}" for f in folders]

    # Go through every folder in folders
    for folder in folders[1:2]:

        # Get session files in folder
        session_files = [f for f in os.listdir(folder) if f.endswith(".csv")]

        # Some session files must be found to proceed
        # assert len(session_files) > 0, 'No session files found.'
        if len(session_files) <= 0:
            continue

        # Go through every session file
        for s_file in session_files:
            # Load session
            raw_session_df = pd.read_csv(
                folder + "/" + s_file, usecols=["Timestamp", "Station", "Sensor", "PM2.5", "Session Id"]
            )
            rows = []

            # Get session id
            session_id = raw_session_df.iloc[0]["Session Id"]

            # Get all station names
            stations = raw_session_df["Station"].unique()

            # Go through all stations
            for station in stations:
                station_df = raw_session_df[raw_session_df["Station"] == station]

                # Get median timestamp and PM2.5
                timestamp = get_middle_value(station_df, "Timestamp")
                PM2_5 = get_middle_value(station_df, "PM2.5")

                # Combine sensors into single column
                sensors = sorted(list(station_df["Sensor"].unique()))
                sensors = "".join([str(s) for s in sensors])

                # Create row
                rows.append([session_id, timestamp, station, PM2_5, sensors])

            # Combine all stations into one "averaged" session dataframe
            session_df = pd.DataFrame(rows, columns=["Session Id", "Timestamp", "Station", "PM2.5", "Sensors"])

            # Add to all sessions
            sessions.append(session_df)

    # Combine sessions into one dataframe
    sessions_df = pd.concat(sessions)
    sessions_df.reset_index(drop=True, inplace=True)

    # Return sessions df
    return sessions_df


################################
# SETUP
################################

sessions_df = algorithm_1_sessions()
