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
import sys

from src.util import *
from src.frames import *

################################
# MAIN
################################


def merge_sensirion_sensors(
    input_file="../results/sessions/sensirion_raw.csv", output_file="../results/sessions/sensirion.csv"
):
    """Merges raw sensor values for each sensor."""

    r_df = pd.read_csv(input_file)

    column_order = [
        "Session Id",
        "Timestamp",
        "Period",
        "Station",
        "Sensors",
        "NC0.5",
        "NC1.0",
        "NC2.5",
        "NC10",
        "TypicalParticleSize",
        "PM1.0",
        "PM2.5",
        "PM4.0",
        "PM10",
        "Temperature",
        "Humidity",
        "Date",
        "Time",
    ]

    sessions = []

    for session_id, session in r_df.groupby("Session Id"):
        # Get the mean of all data columns
        mean_df = session.groupby(["Station"]).mean()

        # Add meta data to dataframe
        mean_df["Sensors"] = "".join(list(session["Sensor"].unique()))
        mean_df["Session Id"] = session_id
        mean_df["Station"] = mean_df.index

        # Reset index from stations to numbers
        mean_df = mean_df.reset_index(drop=True)

        # Go through every station and add timedata
        station_times = {}

        for station, grp in session.groupby("Station"):

            # Get time data
            timestamp = get_middle_value(grp, "Timestamp")
            date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            time = timestamp[-8:]

            station_times[station] = {"Timestamp": timestamp, "Date": date, "Time": time}

        # Add time data to dataframe
        tf = pd.DataFrame.from_dict(station_times).T
        tf["Station"] = tf.index
        tf = tf.reset_index(drop=True)

        mean_df = pd.merge(mean_df, tf, on=["Station"])

        # Add session to total session
        sessions.append(mean_df)

    # Combine sessions into one dataframe
    sessions_df = pd.concat(sessions)
    sessions_df.reset_index(drop=True, inplace=True)

    # Convert timestamp string column into datetime
    sessions_df["Timestamp"] = sessions_df["Timestamp"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))

    # Add period label
    sessions_df["Period"] = sessions_df["Time"].apply(
        lambda x: "Morning rush" if morning(x) else "Evening rush" if evening(x) else "Offtime"
    )

    # Reorder columns
    sessions_df = sessions_df[column_order]

    # Save to csv
    sessions_df.to_csv(output_file, index=False)
    print(f"Sensirion data saved to {output_file}")


def merge_disc_sensor(input_file="../results/sessions/disc_raw.csv", output_file="../results/sessions/disc.csv"):
    """Merges raw sensor values for each sensor."""

    # r_df = pd.read_csv("../results/sessions/disc_raw.csv")
    r_df = combine_raw_session_dfs("../data/sessions/DiSC", "../results/sessions/disc_raw.csv")

    column_order = [
        "Session Id",
        "Timestamp",
        "Period",
        "Station",
        "Sensors",
        "Number",
        "Size",
        "LDSA",
        "Filter",
        "Diff",
        "Date",
        "Clock Time",
        "Time",
    ]

    sessions = []

    for session_id, session in r_df.groupby("Session Id"):
        # Convert to int
        session["Size"] = session["Size"].apply(lambda x: float(x.replace(",", ".")))
        session["LDSA"] = session["LDSA"].apply(lambda x: float(x.replace(",", ".")))
        session["Diff"] = session["Diff"].apply(lambda x: float(x.replace(",", ".")))
        session["Filter"] = session["Filter"].apply(lambda x: float(x.replace(",", ".")))
        # session[["Number", "Size", "LDSA", "Diff", "Filter"]] = session[["Number", "Size", "LDSA", "Diff", "Filter"]].apply(pd.to_numeric)

        # Get the mean of all data columns
        mean_df = session.groupby(["Station"]).mean()

        # Add meta data to dataframe
        mean_df["Sensors"] = "".join(list(session["Sensor"].unique()))
        mean_df["Session Id"] = session_id
        mean_df["Station"] = mean_df.index

        # Reset index from stations to numbers
        mean_df = mean_df.reset_index(drop=True)

        # Go through every station and add timedata
        station_times = {}

        for station, grp in session.groupby("Station"):

            # Get time data
            timestamp = get_middle_value(grp, "Timestamp")

            if type(timestamp) != str:
                timestamp = str(timestamp)

            date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            time = timestamp[-8:]

            station_times[station] = {"Timestamp": timestamp, "Date": date, "Clock Time": time}

        # Add time data to dataframe
        tf = pd.DataFrame.from_dict(station_times).T
        tf["Station"] = tf.index
        tf = tf.reset_index(drop=True)

        mean_df = pd.merge(mean_df, tf, on=["Station"])

        # Add session to total session
        sessions.append(mean_df)

    # Combine sessions into one dataframe
    sessions_df = pd.concat(sessions)
    sessions_df.reset_index(drop=True, inplace=True)

    # Convert timestamp string column into datetime
    sessions_df["Timestamp"] = sessions_df["Timestamp"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))

    # Add period label
    sessions_df["Period"] = sessions_df["Clock Time"].apply(
        lambda x: "Morning rush" if morning(x) else "Evening rush" if evening(x) else "Offtime"
    )

    # Reorder columns
    sessions_df = sessions_df[column_order]

    # Save to csv
    sessions_df.to_csv(output_file, index=False)
    print(f"Sensirion data saved to {output_file}")


if __name__ == "__main__":

    def usage():
        print("Usage: python merge_sessions.py [sensirion|disc]")
        sys.exit()

    if len(sys.argv) < 2:
        usage()

    # Get first argument
    sensor_type = sys.argv[1].lower()

    if sensor_type not in ["sensirion", "disc"]:
        usage()

    if sensor_type == "sensirion":
        merge_sensirion_sensors()

    if sensor_type == "disc":
        merge_disc_sensor()
