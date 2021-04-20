from invoke import task
from tasks.util.env import PROJ_ROOT
from os.path import join
import matplotlib.pyplot as plt
import pandas as pd

import matplotlib

matplotlib.use("tkagg")

RESULTS_DIR = join(PROJ_ROOT, "results")


@task
def plot(ctx):
    """
    Plot the covid results
    """
    native_csv = join(RESULTS_DIR, "covid", "covid_native.csv")
    results = pd.read_csv(native_csv)

    # Average over runs
    grouped = results.groupby("Threads")
    times = grouped.mean()
    errs = grouped.std()

    # Plot all three times
    times.plot.line(
        y="Setup", yerr=errs, ecolor="gray", elinewidth=0.8, capsize=1.0
    )

    times.plot.line(
        y="Execution", yerr=errs, ecolor="gray", elinewidth=0.8, capsize=1.0
    )

    times.plot.line(
        y="Total", yerr=errs, ecolor="gray", elinewidth=0.8, capsize=1.0
    )

    plt.title("CovidSim run time")
    plt.legend(["Native"])
    plt.ylabel("Time (s)")
    plt.show()
