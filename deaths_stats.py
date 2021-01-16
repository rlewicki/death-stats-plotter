import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np


def get_deaths(data):
    deaths = []
    for entry in data:
        entry_str =  entry[4].replace(" ", "")
        if entry_str != ":":
            death_count = int(entry_str)
            deaths.append(death_count)
    return deaths


def adjust_death_data(death_data, target_count):
    while len(death_data) != target_count:
        if len(death_data) < target_count:
            death_data.append(0)
        else:
            death_data = death_data[:-1]
    return death_data


pp = PdfPages("deahts_by_year_eu.pdf")
data = open("demo_r_mwk_ts_1_Data.csv", "r")
entries = []
labels = data.readline()
for line in data:
    line = line.replace("\n", "")
    line = line.replace("\"", "")
    entries.append(line.split(","))

query_countries = ["Belgium",
"Bulgaria",
"Czechia",
"Denmark",
"Germany (until 1990 former territory of the FRG)",
"Estonia",
"Greece",
"Spain",
"France",
"Croatia",
"Italy",
"Cyprus",
"Latvia",
"Lithuania",
"Luxembourg",
"Hungary",
"Malta",
"Netherlands",
"Austria",
"Poland",
"Portugal",
"Romania",
"Slovenia",
"Slovakia",
"Finland",
"Sweden",
"United Kingdom",
"Iceland",
"Liechtenstein",
"Norway",
"Switzerland",
"Montenegro",
"Albania",
"Serbia",
"Andorra",
"Armenia",
"Georgia"]
query_sex = "Total" # Males, Females, Total

for query_country in query_countries:
    queried_data = []
    for entry in entries:
        if entry[2] == query_sex and entry[1] == query_country:
            queried_data.append(entry)

    queried_data = queried_data[:-1]
    data_prev_year = queried_data[:(len(queried_data) // 2)]
    data_prev_year = data_prev_year[:-1]
    data_cur_year = queried_data[(len(queried_data) // 2):]

    y_labels = []
    for i in range(len(data_cur_year)):
        y_labels.append(i + 1)

    target_weeks = 53
    prev_deaths = get_deaths(data_prev_year)
    cur_deaths = get_deaths(data_cur_year)
    prev_deaths = adjust_death_data(prev_deaths)
    cur_deaths = adjust_death_data(cur_deaths)

    x = np.arange(len(y_labels))
    width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, prev_deaths, width, label="2019")
    rects2 = ax.bar(x + width / 2, cur_deaths, width, label="2020")

    ax.set_ylabel("Deaths")
    ax.set_title("Deaths by year - " + query_country)
    ax.legend()
    pp.savefig(fig)
    plt.close(fig)

pp.close()
