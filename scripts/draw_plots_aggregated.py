import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_PATH = os.getcwd()
HOURS = 120

COVERAGE_FILE_NAME = "coverage.csv"
OUTPUT_FILE_NAME = "coverage_subsys.png"

SUBSYSTEMS = {
    "skbuff.c": "net/core/skbuff.c",
    "socket.c": "net/socket.c",
    "ipv4": "net/ipv4/",
    "tcp": "net/ipv4/tcp_",
    "netfilter": "net/ipv4/netfilter/",
    "routing": "net/ipv4/fib_"
}

if not os.path.exists(os.path.join(BASE_PATH, COVERAGE_FILE_NAME)):
    print("coverage.csv not found. Run gen_coverage_csv.py first.")
    exit(1)

coverage_table = pd.read_csv(os.path.join(BASE_PATH, COVERAGE_FILE_NAME), sep=",")

# Calculate coverage for each subsystem.
# Drop rows that don't belong to any subsystem.
# Then, plot the coverage trend of each subsystem by time in a single plot.

# Drop rows that don't belong to any subsystem
coverage_table = coverage_table[coverage_table["Filename"].str.startswith(tuple(SUBSYSTEMS.values()))]

subsys_dfs = []

for subsys in SUBSYSTEMS:
    # Filter rows
    df = coverage_table[coverage_table["Filename"].str.startswith(SUBSYSTEMS[subsys])]
    df = df.drop(["Filename", "Function"], axis=1)

    df = df.groupby(["time_diff"]).sum()
    df = df.reset_index()

    # Calculate (Covered PCs / Total PCs) for each row and save as new column 'Coverage'
    df["Coverage"] = df["Covered PCs"] / df["Total PCs"]

    # Drop columns 'Covered PCs' and 'Total PCs'
    df = df.drop(["Covered PCs", "Total PCs"], axis=1)

    # Add column 'Subsystem'
    df["Subsystem"] = subsys

    # Add to list
    subsys_dfs.append(df)

# Draw plot
fig, ax = plt.subplots(figsize=(10, 6))

for df in subsys_dfs:
    ax.plot(df["time_diff"], df["Coverage"], label=df["Subsystem"].iloc[0])

# Customize the plot
ax.set_title("Coverage of subsystems")
ax.set_xlabel("Time (hours)")
ax.set_ylabel("Coverage")
# ax.set_ylim(0, 1.1)
ax.set_xlim(0, HOURS)
ax.grid(True)

# Move the legend outside the plot area
ax.legend(title="Subsystem", bbox_to_anchor=(1.05, 1), loc='upper left')

# Adjust layout to prevent cropping
plt.tight_layout()
plt.subplots_adjust(right=0.75)  # Fine-tune the spacing

# Save plot
plt.savefig(os.path.join(BASE_PATH, OUTPUT_FILE_NAME), dpi=300)
plt.show()
