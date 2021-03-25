import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys

NATIVE_DATA_FILE = "covid_native.dat"
FAASM_DATA_FILE = "covid_native.dat"
OUT_FILE = "covid.png"

test_data = {1: [10.883981, 10.776523000000001], 10: [27.986638, 27.214199999999998], 20: [49.723203999999996, 60.012849]}


def _load_results():
    with open(NATIVE_DATA_FILE) as json_file:
        native_results = json.load(json_file)
    with open(FAASM_DATA_FILE) as json_file:
        faasm_results = json.load(json_file)
    return native_results, faasm_results


def _do_avg(result_array):
    return float(sum(result_array) / len(result_array))


def _do_stdev(result_array):
    sum_pow_2 = sum([x**2 for x in result_array])
    n = len(result_array)
    return float(sum_pow_2/n) - pow(_do_avg(result_array), 2)


def main():
    native_results, faasm_results = _load_results()

    # Define the independent variables
    labels = list(native_results.keys())
    # num_hosts = TODO depending on faasm results
    xs = labels
    xmin = xs[0]
    xmax = xs[-1] * 3
    # TODO handle the multi-host case
    print(labels)

    # Define the dependent variables
    fig, ax = plt.subplots()
    y_native = [_do_avg(native_results[key]) for key in native_results.keys()]
    y_native_min = min(y_native)
    yerr_native = [_do_stdev(native_results[key]) for key in native_results.keys()]
    print(yerr_native)
    plt.errorbar(xs, y_native, yerr_native, marker=".", label="Native")

    # Horizontal line indicating the absolute minimum we achieve w/ one machine
    plt.axhline(y=y_native_min, color="orange", linestyle="--")
    # Vertical lines every <cpu_count>
    for _x in [ind for ind,val in enumerate(list(faasm_results.keys())) if int(val) % 20 == 0]:
        plt.axvline(x=_x, linestyle="dashed", color="gray")
    plt.xlim(xmin, xmax)

    # Plot aesthetics
    ax.legend()
    ax.set_xticks(xs)
    ax.set_xticklabels(labels)
    ax.set_xlabel("# OpenMP Threads")
    ax.set_ylabel("Average elapsed time [seconds] + Stdev")
    ax.set_title("CovidSim time to completion Faasm vs Native")
    fig.tight_layout()
    plt.savefig(OUT_FILE)


if __name__ == "__main__":
    main()