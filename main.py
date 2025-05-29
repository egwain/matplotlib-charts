from datetime import datetime
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

def parseCsvData(filename: str) -> tuple[list[datetime], dict[str, list[float]]]:
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

def nextColor(i: int, defaultColor: str = "pink"):
    colors = ["green", "royalblue", "red", "orange", "deepskyblue", "blueviolet", "lime", "black", "gray", "darkgray"]
    try:
        return colors[i]
    except IndexError:
        return defaultColor

def generateChart(x: list[datetime], y: dict[str, list[float]], overviewLines: list[str] = []):
    fig, ((ax1)) = plt.subplots(nrows=1, ncols=1, figsize=(14, 8))

    for i, key in enumerate(y.keys()):
        if key in overviewLines:
            ax1.plot(x, y[key], ':', linewidth=2, label=key, marker=None, color=nextColor(i))
        else:
            ax1.plot(x, y[key], '-', linewidth=2, label=key, marker='.', color=nextColor(i))

    ax1.set_title('Overview')
    ax1.legend(fancybox=True, shadow=True, loc='upper left', fontsize='small', frameon=True)
    ax1.grid(color='grey', linestyle=':', linewidth=0.5)
    
    formatter = ticker.StrMethodFormatter('{x:.0f} Kč')#{x:,.0f}
    ax1.yaxis.set_major_formatter(formatter)
    
    plt.show()

def createOverviewLine(x: list[datetime], y: dict[str, list[float]], excludeKeys: list[str] = []):
    result = []
    for i in range(len(x)):
        sum = 0
        for key in y.keys():
            if key in excludeKeys:
                continue
            sum += y[key][i] if y[key][i] is not None else 0
        result.append(sum)
    return result
    
x, y = parseCsvData("data.csv")
# print(y)
total = createOverviewLine(x, y)
total2 = createOverviewLine(x, y, excludeKeys=["Spor. ucty"])
y["Total"] = total
y["Inv. Total"] = total2
generateChart(x, y, ["Total", "Inv. Total"])