"""
sessions.py

Session functions for Stockholm Air Pollution project.
"""

################################
# LIBRARIES
################################
import pandas as pd
import numpy as np

from src.util import *

################################
# FRAMES FUNCTIONS
################################


def get_sensor_dfs(date, sensors, period):
    # Load data
    dfs = []
    labels = []

    dir_files = os.listdir(f"../data/sensor_data/{date}/")
    data_files = []

    for file in dir_files:
        if (file[0] in sensors) and (file.endswith(f"{period}.csv")):
            data_files.append(file)

    data_files.sort()

    # Add timestamps column
    for file in data_files:
        df = pd.read_csv(f"../data/sensor_data/{date}/{file}", skiprows=1)
        df["Timestamp"] = df["Time"].apply(lambda x: format_time(date, x) + timedelta(hours=2))

        # Add label column
        df["Sensor"] = file[0]

        dfs.append(df)

        labels.append(file.split("-")[0])

    return dfs, labels, data_files


def combine_raw_session_dfs(data_folder="../data/sensor_data"):
    """Combines all raw station records into one dataframe and returns it."""

    # Store all raw session dataframes in array
    session_dfs = []

    # Get all date folders
    folders = get_folder_paths(data_folder)

    # Go through every folder in folders
    for folder in folders:

        # Get session files in folder
        session_files = [f for f in os.listdir(folder) if f.endswith(".csv")]

        # Some session files must be found to proceed
        if len(session_files) <= 0:
            continue

        # Go through every session file
        for s_file in session_files:
            # Load raw session dataframe
            raw_df = pd.read_csv(folder + "/" + s_file, index_col=0)

            session_dfs.append(raw_df)

    # Combine into one big session df
    df = pd.concat(session_dfs)

    # Remove unnamed column and reset index
    # df.drop("Unnamed: 0", axis=1, inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Convert timestamp string column into datetime
    df["Timestamp"] = df["Timestamp"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))

    # Return dataframe
    return df


def get_computed_sessions(data_folder="../data/sensor_data", disc=False):
    """
    Goes through all sessions and takes the median value for every station record.

    Per session:
    Convert all station data into one record.

    Timestamp: round((tmin + tmax) / 2)
    Station: same
    Sensors: all sensors involved
    Pm2.5: median
    Session id: same
    """

    # Save all sessions in array
    sessions = []

    # Get all date folders
    folders = get_folder_paths(data_folder)

    # Go through every folder in folders
    for folder in folders:

        # Get session files in folder
        session_files = [f for f in os.listdir(folder) if f.endswith(".csv")]

        # Some session files must be found to proceed
        if len(session_files) <= 0:
            continue

        # Go through every session file
        for s_file in session_files:
            # Load session
            raw_session_df = pd.read_csv(folder + "/" + s_file)
            rows = []

            # Get session id
            session_id = raw_session_df.iloc[0]["Session Id"]

            # Get all station names
            stations = raw_session_df["Station"].unique()

            # Go through all stations
            for station in stations:
                # Get all rows corresponding to the station
                station_df = raw_session_df[raw_session_df["Station"] == station]

                # Get median timestamp
                timestamp = get_middle_value(station_df, "Timestamp")

                # Split station_df into different sensors
                sensors = sorted(list(station_df["Sensor"].unique()))

                if disc:
                    number_counts = np.array([])
                else:
                    # Save median PM2_5
                    pm2_5s = np.array([])
                    nc2_5s = np.array([])

                for sensor in sensors:
                    # Pick out sensor df
                    sensor_df = station_df[station_df["Sensor"] == sensor]

                    if disc:
                        # Get median for sensor
                        number_counts = np.append(number_counts, get_middle_value(sensor_df, "Number"))
                    else:
                        # Get median for sensor
                        pm2_5s = np.append(pm2_5s, get_middle_value(sensor_df, "PM2.5"))
                        nc2_5s = np.append(nc2_5s, get_middle_value(sensor_df, "NC2.5"))

                if disc:
                    NUMBER_COUNT = np.mean(number_counts)
                else:
                    # Take mean of all PM values
                    PM2_5 = np.mean(pm2_5s)
                    NC2_5 = np.mean(nc2_5s)

                # Combine sensors into single label
                sensors_label = "".join([str(s) for s in sensors])

                # Create row
                date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").time()

                if disc:
                    rows.append([session_id, timestamp, date, time, station, NUMBER_COUNT, sensors_label])
                else:
                    rows.append([session_id, timestamp, date, time, station, PM2_5, NC2_5, sensors_label])

            # Combine all stations into one "averaged" session dataframe
            if disc:
                session_df = pd.DataFrame(
                    rows, columns=["Session Id", "Timestamp", "Date", "Time", "Station", "Number", "Sensors"]
                )
            else:
                session_df = pd.DataFrame(
                    rows, columns=["Session Id", "Timestamp", "Date", "Time", "Station", "PM2.5", "NC2.5", "Sensors"]
                )

            # Add to all sessions
            sessions.append(session_df)

    # Combine sessions into one dataframe
    sessions_df = pd.concat(sessions)
    sessions_df.reset_index(drop=True, inplace=True)

    # Convert timestamp string column into datetime
    sessions_df["Timestamp"] = sessions_df["Timestamp"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))

    # Return sessions df
    return sessions_df


def get_calibrate_df(date, folder):
    # Store all raw session dataframes in array
    calibrate_dfs = []

    # Get session files in folder
    session_files = sorted(os.listdir(folder))

    for i, file_name in enumerate(session_files):

        # Read individual sensor data
        raw_df = pd.read_csv(folder + "/" + file_name, skiprows=1)
        raw_df["Sensor"] = str(file_name[0])
        raw_df["Timestamp"] = raw_df["Time"].apply(lambda x: format_time(date, x) + timedelta(hours=2))

        # Remove first 150 rows and last 30 rows
        raw_df = raw_df[150:]
        raw_df = raw_df[:-30]

        # Add to list
        calibrate_dfs.append(raw_df)

    # Combine all sensor dfs into one large dataframe
    calibrate_df = pd.concat(calibrate_dfs)
    calibrate_df.reset_index(drop=True, inplace=True)

    return calibrate_df
