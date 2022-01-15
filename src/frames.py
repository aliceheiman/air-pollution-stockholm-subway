"""
sessions.py

Session functions for Stockholm Air Pollution project.
"""

################################
# LIBRARIES
################################
import pandas as pd
import numpy as np
import re

from src.util import *

################################
# FRAMES FUNCTIONS
################################


def get_sensor_dfs(date, sensors, period, use_all=False):
    # Load data
    dfs = []
    labels = []

    dir_files = os.listdir(f"../data/sensor_data/{date}/")
    data_files = []

    for file_name in dir_files:
        if use_all == True and file_name.lower().endswith(".csv"):
            data_files.append(file_name)
        else:
            if (file_name[0] in sensors) and (file_name.endswith(f"{period}.csv")):
                data_files.append(file_name)

    data_files.sort()

    # Add timestamps column
    for file_name in data_files:
        df = pd.read_csv(f"../data/sensor_data/{date}/{file_name}", skiprows=1)
        df["Timestamp"] = df["Time"].apply(lambda x: format_time(date, x) + timedelta(hours=2))

        # Add label column
        df["Sensor"] = file_name[0]

        dfs.append(df)

        labels.append(file_name.split("-")[0])

    return dfs, labels, data_files


def get_disc_df(date, filepath, offset=60):
    """[summary]

    Returns:
        dataframe:
    """

    def fix_timestamp(x):
        if ".500" in str(x):
            return datetime.strptime(str(x)[0:19], "%Y-%m-%d %H:%M:%S")
        else:
            return x

    disc_df = pd.read_csv(filepath, sep="\t", skiprows=5)
    disc_df = disc_df.iloc[:, :-1]  # remove last column
    disc_df["Time"] = disc_df["Time"].apply(lambda x: float(x.replace(",", ".")))  # use . as decimal delimiter

    # Get start time
    with open(filepath) as f:
        contents = f.readlines()

    match = re.search(r"\d{2}:\d{2}:\d{2}", contents[3])
    start_time = match.group()

    # Add timestamp column
    str_time = date + " " + start_time
    initial_timestamp = datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")

    # Get absolute time and offset 60 due to calibration
    disc_df["Timestamp"] = disc_df["Time"].apply(lambda x: add_secs(initial_timestamp, x + offset))

    # Fix timestamps to whole seconds
    disc_df["Timestamp"] = disc_df["Timestamp"].apply(lambda x: fix_timestamp(x))

    # Add sensor column
    disc_df["Sensor"] = "DiSC"

    return disc_df


def combine_raw_session_dfs(data_folder="../data/sessions/Sensirion", output_name=False):
    """Combines all raw station records into one dataframe and returns it."""

    # Store all raw session dataframes in array
    session_dfs = []

    # Get all date folders
    folders = get_folder_paths(data_folder)

    # Go through every folder in folders
    for folder in folders:

        # Get session files in folder
        session_files = [f for f in os.listdir(folder) if f.lower().endswith(".csv")]

        # Some session files must be found to proceed
        if len(session_files) <= 0:
            continue

        # Go through every session file
        for s_file in session_files:
            # Load raw session dataframe
            raw_df = pd.read_csv(f"{folder}/{s_file}", index_col=0)

            session_dfs.append(raw_df)

    # Combine into one big session df
    df = pd.concat(session_dfs)

    # Remove unnamed column and reset index
    # df.drop("Unnamed: 0", axis=1, inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Convert timestamp string column into datetime
    df["Timestamp"] = df["Timestamp"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))

    if output_name:
        df.to_csv(output_name, index=False)

    return df


def get_computed_sessions(data_folder="../data/sessions/Sensirion", disc=False, output_name=False):
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
    if output_name:
        sessions_df.to_csv(output_name, index=False)
    else:
        return sessions_df


def get_calibrate_df(date, folder):
    # Store all raw dataframes in array
    calibrate_dfs = []

    # Get sensirion files in folder
    sensor_files = sorted(os.listdir(folder))
    sensirion_files = [s for s in sensor_files if s.lower().endswith(".csv")]

    for i, file_name in enumerate(sensirion_files):

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


def get_total_measurement_time(data_folder="../data/sensor_data", output_name=False):
    """Computes the total measurement time for each sensor.

    Args:
        input_name (str, optional): [description]. Defaults to '../data/sensor_data'.
        output_name (bool, optional): [description]. Defaults to False.
    """

    # Get all measurement times for the different sensors
    sensor_times = {}

    # Get all date folders
    folders = get_folder_paths(data_folder)

    # Go through every folder and get sensor dfs
    for folder in folders:
        date = folder[-10:]
        s_dfs, labels, data_files = get_sensor_dfs(date, sensors=[], period="", use_all=True)

        s_df = pd.concat(s_dfs)
        for sensor, grp in s_df.groupby("Sensor"):
            if sensor not in sensor_times:
                # Initialize to zero seconds
                sensor_times[sensor] = 0

            # Get number of rows and add
            sensor_times[sensor] += len(grp)

    # Turn into pandas dataframe
    measurement_df = pd.DataFrame(sensor_times.items(), columns=["Sensor", "Seconds"])
    measurement_df["Sensor"] = measurement_df["Sensor"].astype(str)

    # Save to
    if output_name:
        measurement_df.to_csv(output_name, index=False)
    else:
        return measurement_df


def get_measuring_time(data_folder="../data/sensor_data", output_name=False):
    """Computes the measurement time THE RESEARCHERS were on the platform.

    Args:
        input_name (str, optional): [description]. Defaults to '../data/sensor_data'.
        output_name (bool, optional): [description]. Defaults to False.
    """

    # Get all measurement times for the different sensors
    date_times = {}

    # Get all date folders
    folders = get_folder_paths(data_folder)

    # Go through every folder and get sensor dfs
    for folder in folders:
        date = folder[-10:]
        s_dfs, labels, data_files = get_sensor_dfs(date, sensors=[], period="", use_all=True)

        s_df = pd.concat(s_dfs)
        for sensor, grp in s_df.groupby("Sensor"):
            if date not in date_times:
                # Initialize to zero seconds
                date_times[date] = 0

            # Get number of rows and add
            sensor_records = len(grp)

            if sensor_records > date_times[date]:
                date_times[date] = sensor_records

    # Turn into pandas dataframe
    measurement_df = pd.DataFrame(date_times.items(), columns=["Date", "Seconds"])

    # Save to
    if output_name:
        measurement_df.to_csv(output_name, index=False)
    else:
        return measurement_df
