import os
import glob
import pandas as pd

FILENAME_FILTER = ("net/ipv4", "net/core", "net/socket.c")
COVERAGE_FILE_NAME = "coverage.csv"
BASE_PATH = os.getcwd()


def gen_coverage_csv():
    data = {}
    start_time = None
    os.chdir(os.path.join(BASE_PATH, "csv_cover"))
    for f in glob.glob("*.csv"):
        data[f[:-4]] = pd.read_csv(f, sep=",")

    start_time = pd.to_datetime(min(data.keys()), format="%Y_%m_%d_%H_%M_%S")

    # Save filename as column 'Time'
    for key in data:
        data[key]["time_diff"] = (
            pd.to_datetime(key, format="%Y_%m_%d_%H_%M_%S") - start_time
        )
        # Convert to hours
        data[key]["time_diff"] = data[key]["time_diff"].dt.total_seconds() / 3600

    # Concat tables whose 'Time' column is smaller than 120 hours
    filtered_data = {}
    for key in data:
        if data[key]["time_diff"].max() <= 120:
            filtered_data[key] = data[key]
    tbl = pd.concat(data.values(), ignore_index=True)

    # Filter rows
    tbl = tbl[tbl["Filename"].str.startswith(FILENAME_FILTER)]

    # Drop column 'Module'
    tbl = tbl.drop(["Module"], axis=1)

    os.chdir(BASE_PATH)

    return tbl


coverage_table = gen_coverage_csv()
coverage_table.to_csv(os.path.join(BASE_PATH, COVERAGE_FILE_NAME), index=False)
