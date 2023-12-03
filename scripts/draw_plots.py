import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_PATH = os.getcwd()
HOURS = 120

OUTPUT_DIR = "out_" + str(HOURS) + "h"
COVERAGE_FILE_NAME = "coverage.csv"

if not os.path.exists(os.path.join(BASE_PATH, COVERAGE_FILE_NAME)):
    print("coverage.csv not found. Run gen_coverage_csv.py first.")
    exit(1)

coverage_table = pd.read_csv(os.path.join(BASE_PATH, COVERAGE_FILE_NAME), sep=",")

# Calculate (Covered PCs / Total PCs) for each row and save as new column 'Coverage'
coverage_table["Coverage"] = coverage_table["Covered PCs"] / coverage_table["Total PCs"]

# Drop columns 'Covered PCs' and 'Total PCs'
coverage_table = coverage_table.drop(["Covered PCs", "Total PCs"], axis=1)

if not os.path.exists(os.path.join(BASE_PATH, OUTPUT_DIR)):
    os.makedirs(os.path.join(BASE_PATH, OUTPUT_DIR))

# Recursively delete any existing files and directories in OUTPUT_DIR
for root, dirs, files in os.walk(os.path.join(BASE_PATH, OUTPUT_DIR), topdown=False):
    for name in files:
        os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root, name))

for filename in coverage_table["Filename"].unique():
    # Filter rows
    df = coverage_table[coverage_table["Filename"] == filename]
    df = df.drop(["Filename"], axis=1)

    # Make subdirectory for filename
    if not os.path.exists(os.path.join(BASE_PATH, OUTPUT_DIR, filename)):
        os.makedirs(os.path.join(BASE_PATH, OUTPUT_DIR, filename))

    # Draw plot for each function
    for function in df["Function"].unique():
        # Filter rows
        df2 = df[df["Function"] == function]
        df2 = df2.drop(["Function"], axis=1)

        # Sort by time_diff
        df2 = df2.sort_values(by=["time_diff"])

        ax = df2.plot.line(
            x="time_diff", y="Coverage",
            title=function, legend=False, grid=True,
            linewidth=2, color="blue"
        )

        ax.set_ylim((0, 1.1))
        ax.set_ylabel("Coverage")
        ax.set_xlim((0, HOURS))
        ax.set_xlabel("Time (hours)")
        ax.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
        ax.set_xticks(range(0, HOURS + 1, 24))


        # If coverage is 0 for all rows, set flag to False
        save_plot = True
        if df2["Coverage"].max() == 0:
            save_plot = False

        # Save plot
        if save_plot:
            plt.savefig(
                os.path.join(BASE_PATH, OUTPUT_DIR, filename, function + ".png")
            )
        plt.close()

    # If directory is empty, delete it
    if not os.listdir(os.path.join(BASE_PATH, OUTPUT_DIR, filename)):
        os.rmdir(os.path.join(BASE_PATH, OUTPUT_DIR, filename))
