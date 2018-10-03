#!/usr/bin/env python3
# coding: utf-8


""" Explore database """
from hal.data.lists import find_commons
from hal.data.matrix import Matrix
from hal.mongodb.documents import DbBrowser
from hal.streams.pretty_table import pretty_format_table

from statsf1.data import NUM_FORMAT, DNF
from statsf1.tools.utils import pretty_time, parse_time


class Explorer:
    def __init__(self, db):
        self.db_name = db
        self.db = DbBrowser(self.db_name)  # db browser

    def count_races(self):
        return self.db.get_documents_count()

    def average_race_entrants(self):
        races = self.db.get_documents_in_database()
        race_entrants = 0
        key = "race_entrants"

        for race in races:
            if key in race:
                data = race[key]
                race_entrants += len(data["Pilote "])

        return race_entrants / len(races)

    def get_races(self, year):
        collection = self.db.get_documents_in_collection(year)
        return [
            race
            for race in collection
        ]

    def get_year_values(self, year, races, category, label, driver, chassis,
                        position):
        all_races = [
            race
            for race in self.get_races(year)  # all races of year
            if race["name"] in races  # just selected races
        ]
        categories = [
            race[category]
            for race in all_races
        ]  # just selected category
        columns = [
            category[label]
            for category in categories
        ]  # just selected label

        if position is None:  # find by driver or chassis
            if driver is not None:  # find by driver
                position = categories[0]["Pilote "].index(driver)
            else:  # find by chassis
                position = categories[0]["Ch\\xc3\\xa2ssis "].index(chassis)
        values = [
            column[position]
            for column in columns
        ]  # get selected

        return values

    def get_matrix(self, years, races, category, label, driver=None,
                   chassis=None, position=None):
        """
        :param years: [] of str
            Years to get
        :param races: [] of str
            Get all the following races. Raises error if any of the race is
            not found across ALL specified years
        :param category: str
            Race category, e.g "race_entrants", "qualifications" ...
        :param label: str
            Result label, e.g "Tour", "Moyenne", "Pos" ...
        :param driver: str
            Get results of this driver
        :param chassis: str
            Get results of this chassis
        :param position: int
            Get i-th results based on category index, e.g 0 means get the winner
        :return: [] of [] of str
            Each column is a race. Each row is a year. Each cell is the
            result of the label of the category at race of year.
        """

        if driver is None and chassis is None and position is None:
            raise ValueError("driver, chassis or position MUST be specified")

        specified_index = [
            x
            for x in [driver, chassis, position]
            if x is not None
        ]
        if len(specified_index) > 1:
            raise ValueError("exactly 1 among driver, chassis and position "
                             "MUST be specified")
        matrix = [
            self.get_year_values(
                year, races, category, label, driver, chassis, position
            )
            for year in years
        ]

        return matrix

    def get_chassis(self, year):
        races = self.get_races(year)
        chassis = []
        for race in races:
            if "result" in race:
                chassis.append(race["result"]["Ch\\xc3\\xa2ssis "])
        return find_commons(chassis)  # common in all races

    def get_driver(self, year):
        races = self.get_races(year)
        drivers = []
        for race in races:
            if "result" in race:
                drivers.append(race["result"]["Pilote "])
        return find_commons(drivers)  # common in all races


class RaceExplorer(Explorer):
    RACE_SUMMARY_LABELS = ["race pos", "driver", "chassis",
                           "race laps", "race completed?", "race time",
                           "Q pos", "Q time", "race VS Q",
                           "best lap pos", "best lap", "best lap VS Q"]
    DRIVER_SUMMARY_LABELS = ["year", "race pos", "chassis",
                             "race laps", "race completed?", "race time",
                             "Q pos", "Q time", "race VS Q",
                             "best lap pos", "best lap", "best lap VS Q"]
    DNF_RACE = [[DNF] * len(RACE_SUMMARY_LABELS)]

    def __init__(self, race, year, db):
        Explorer.__init__(self, db)

        self.raw_race = str(race)
        self.raw_year = str(year)
        self.race = None

    def get_race(self):
        if self.race is None:
            race = [
                race
                for race in self.get_races(self.raw_year)
                if race["name"] == self.raw_race
            ]

            if race:
                return race[0]

        return self.race

    def get_results(self, key, labels):
        race = self.get_race()
        drivers = race[key]["Pilote "]  # drivers are main key
        data = [
            race[key][label]
            for label in labels
        ]  # find all other data

        data = {
            driver: {
                label: data[j][i]
                for j, label in enumerate(labels)
            }
            for i, driver in enumerate(drivers)
        }

        for driver, labels in data.items():
            if "Pos " in labels:
                try:
                    int(data[driver]["Pos "])  # fix null positions
                except:
                    data[driver]["Pos "] = "ab"

        return data

    def get_drivers(self):
        race = self.get_race()
        return list(set(race["result"]["Pilote "]))

    def get_race_summary(self):
        return self.get_results(
            "result",
            ["Ch\\xc3\\xa2ssis ", "Pos ", "Tour ", "\xa0"]
        )

    def get_qualification_summary(self):
        return self.get_results(
            "qualifications",
            ["Ch\\xc3\\xa2ssis ", "Pos ", "Temps "]
        )

    def get_best_laps_summary(self):
        return self.get_results(
            "best_laps",
            ["Ch\\xc3\\xa2ssis ", "n ", "Temps "]
        )

    def get_summary(self):
        try:
            race = self.get_race_summary()
            qualification = self.get_qualification_summary()
            best_laps = self.get_best_laps_summary()

            standings = sorted(race.items(),
                               key=lambda x: int(x[1]["Pos "], 16))
            race_laps = float(
                race[standings[0][0]]["Tour "])  # laps of the winner
            summary = []

            for driver, _ in standings:
                race_pos = race[driver]["Pos "]
                try:
                    int(race_pos)
                except:
                    race_pos = DNF

                try:
                    race_completed = int(
                        race[driver]["Tour "]) > 0.9 * race_laps
                except:
                    race_completed = False

                if race_completed:
                    race_completed = "yes"
                else:
                    race_completed = "no"

                try:
                    race_time = race[driver]["\xa0"].split("(")[0].strip()
                except:
                    race_time = DNF

                row = [
                    race_pos, driver, race[driver]["Ch\\xc3\\xa2ssis "],
                    race[driver]["Tour "], race_completed, race_time
                ]

                try:
                    q_pos = qualification[driver]["Pos "]
                    q_lap = pretty_time(qualification[driver]["Temps "])
                    q_lap_time = parse_time(q_lap)

                    try:
                        race_vs_q = str(int(race_pos) - int(q_pos))
                    except:
                        race_vs_q = DNF
                except:
                    q_pos = DNF
                    q_lap = DNF
                    q_lap_time = 0
                    race_vs_q = DNF

                row += [q_pos, q_lap, race_vs_q]

                try:
                    best_lap_pos = best_laps[driver]["n "]
                    best_lap = pretty_time(best_laps[driver]["Temps "])
                    best_lap_time = parse_time(best_lap)
                    ratio_best_q = 100.0 * (best_lap_time / q_lap_time - 1)
                    ratio_best_q = NUM_FORMAT.format(ratio_best_q) + "%"
                except:
                    best_lap_pos = DNF
                    best_lap = DNF
                    ratio_best_q = DNF

                row += [best_lap_pos, best_lap, ratio_best_q]
                summary.append(row)
        except:
            summary = self.DNF_RACE

        return self.RACE_SUMMARY_LABELS, summary

    def get_previous_years_results(self, n_years):
        year = int(self.raw_year)
        years = range(year - n_years + 1, year + 1)

        return self.RACE_SUMMARY_LABELS, {
            str(year):
                RaceExplorer(
                    self.raw_race, str(year), self.db_name
                ).get_summary()[1]
            for year in years
        }

    def get_previous_years_matrix(self, n_years, driver):
        labels, summaries = self.get_previous_years_results(n_years)
        data = {
            year: [row for row in table if row[1] == driver]
            for year, table in summaries.items()
        }
        data = {
            year: row[0] if row else [DNF] * len(labels)
            for year, row in data.items()
        }

        table = [
            [year] + [row[0]] + row[2:]  # remove driver column
            for year, row in data.items()
        ]
        table = list(reversed(table))  # from nearest result to oldest

        return self.DRIVER_SUMMARY_LABELS, table

    def get_results_on(self, year):
        races = [
            race["name"] for race in Explorer(self.db_name).get_races(year)
        ]  # year's race names

        return races, [
            RaceExplorer(race, year, self.db_name).get_summary()
            for race in races
        ]

    def get_results_of_label_on(self, label, year, driver=None, chassis=None):
        names, races = self.get_results_on(year)
        results = [
            race[1]  # first element are the labels
            for race in races
        ]
        labels = races[0][0]
        column = labels.index(label)  # find which column to get

        label_results = {
            name: result
            for name, result in zip(names, results)
        }  # race name -> race result

        for name, race in label_results.items():
            if race[0][0] != DNF:
                try:
                    col_index = None
                    if driver is not None:
                        col_index = Matrix(race).get_column(1).index(driver)

                    if chassis is not None:
                        col_index = Matrix(race).get_column(2).index(chassis)

                    data_column = Matrix(race).get_column(column)
                    if col_index is not None:
                        data_column = [data_column[col_index]]

                    label_results[name] = data_column
                except:
                    label_results[name] = [DNF]  # DNF race
            else:
                label_results[name] = [DNF]  # discard DNFs races

        return label_results


def print_averages(db):
    driver = Explorer(db)
    tot_races = driver.count_races()
    average_drivers = driver.average_race_entrants()
    tot_entries = tot_races * 4 * average_drivers

    message = "{} races and on average {:.2f} drivers -> {} total entries"
    print(message.format(tot_races, average_drivers, tot_entries))


def print_available_races(db, year):
    driver = Explorer(db)
    races = driver.get_races(str(year))
    races = sorted([
        race["name"]
        for race in races
    ])
    print(races)


def run(db):
    driver = RaceExplorer("Japon", 2011, db)
    labels, summary = driver.get_summary()
    print(pretty_format_table(labels, summary))
