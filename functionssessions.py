"""
sessions.py

Session functions for Stockholm Air Pollution project.
"""

################################
# LIBRARIES
################################
from functionshelper import *

################################
# SESSIONS FUNCTIONS
################################


def combine_raw_session_dfs(data_folder="sessions_NC"):
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
    df = df.reset_index(drop=True, inplace=True)

    # Convert timestamp string column into datetime
    df["Timestamp"] = df["Timestamp"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))

    # Return dataframe
    return df


def get_computed_sessions(data_folder="sessions_NC"):
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

                # Save median PM2_5
                pm2_5s = np.array([])

                for sensor in sensors:
                    # Pick out sensor df
                    sensor_df = station_df[station_df["Sensor"] == sensor]

                    # Get median for sensor
                    pm2_5s = np.append(pm2_5s, get_middle_value(sensor_df, "PM2.5"))

                # Take mean of all PM values
                PM2_5 = np.mean(pm2_5s)

                # Combine sensors into single label
                sensors_label = "".join([str(s) for s in sensors])

                # Create row
                date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").time()

                rows.append([session_id, timestamp, date, time, station, PM2_5, sensors_label])

            # Combine all stations into one "averaged" session dataframe
            session_df = pd.DataFrame(
                rows, columns=["Session Id", "Timestamp", "Date", "Time", "Station", "PM2.5", "Sensors"]
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
