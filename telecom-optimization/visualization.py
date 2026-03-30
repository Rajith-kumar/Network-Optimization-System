import matplotlib.pyplot as plt

def plot_load(stations_before, stations_after):
    ids = stations_before["id"]

    before_load = stations_before["load"]
    after_load = stations_after["load"]

    x = range(len(ids))

    plt.figure()

    plt.bar(x, before_load, width=0.4, label="Before", align="center")
    plt.bar([i + 0.4 for i in x], after_load, width=0.4, label="After", align="center")

    plt.xlabel("Base Station ID")
    plt.ylabel("Load")
    plt.title("Load Before vs After Optimization")
    plt.legend()

    plt.show()


def plot_congestion(stations_before, stations_after):
    before = stations_before["congested"].sum()
    after = stations_after["congested"].sum()

    labels = ["Before", "After"]
    values = [before, after]

    plt.figure()
    plt.bar(labels, values)

    plt.ylabel("Number of Congested Stations")
    plt.title("Congestion Comparison")

    plt.show()