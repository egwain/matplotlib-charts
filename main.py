from datetime import datetime
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

def parseCsvData(filename: str):
    x = []
    y = {}
    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            for i, key in enumerate(row.keys()):
                if i == 0:
                    x.append(datetime.strptime(row[key], "%d.%m.%Y"))
                else:
                    value = float(row[key]) if row[key] else None
                    if key not in y:
                        y[key] = [value]
                    else:
                        y[key].append(value)
    return x, y

def getNextPlotColor(i: int, defaultColor: str = "pink"):
    colors = ["green", "royalblue", "red", "orange", "deepskyblue", "blueviolet", "lime", "black", "gray"]
    try:
        return colors[i]
    except IndexError:
        return defaultColor

def generateChart(x, y):
    fig, ((ax1)) = plt.subplots(nrows=1, ncols=1, figsize=(14, 8))

    for i, key in enumerate(y.keys()):
        ax1.plot(x, y[key], '-', linewidth=2, label=key, marker='.', color=getNextPlotColor(i))

    ax1.set_title('Overview')
    ax1.legend(fancybox=True, shadow=True, loc='upper left', fontsize='small', frameon=True)
    ax1.grid(color='grey', linestyle=':', linewidth=0.5)
    
    formatter = ticker.StrMethodFormatter('{x:.0f} Kč')#{x:,.0f}
    ax1.yaxis.set_major_formatter(formatter)
    
    plt.show()

x, y = parseCsvData("data.csv")
# print(y)
generateChart(x, y)