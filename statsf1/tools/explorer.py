#!/usr/bin/env python3
# coding: utf-8


""" Explore database """
from hal.data.lists import find_commons
from hal.data.matrix import Matrix
from hal.mongodb.documents import DbBrowser
from hal.streams.pretty_table import pretty_format_table

from statsf1.data import DNF
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

    def get_race_by_name(self, year, race_name):
        races = [
            race
            for race in self.get_races(year)
            if race["name"] == race_name
        ]

        return races[0]

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

    def get_race_data(self, year, race, category, labels):
        """
        :param year: str
            Browse this year
        :param race: str
            Browse this race
        :param category: str
            Race category, e.g "race_entrants", "qualifications" ...
        :param labels: [] of str
            Result labels, e.g ["Tour", "Moyenne"] ...
        :return: [] of [] of str
            Category results of selected labels
        """

        race = self.get_race_by_name(year, race)
        category = race[category]
        columns = [
            category[label]
            for label in labels
        ]

        return columns

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

    @staticmethod
    def _order_by_drivers(original_drivers, column, drivers):
        """
        :param original_drivers: [] of str
            List of drivers in column
        :param column: [] of anything
            List of data
        :param drivers: [] of str
            List of drivers to order by
        :return: [] of anything
            Data column ordered by drivers
        """

        ordered_column = []

        for driver in original_drivers:
            index = drivers.index(driver)
            value = column[index]

            ordered_column.append(value)

        return ordered_column

    def get_race_summary(self, drivers=None):
        """
        :param drivers: [] of str
            List of drivers to order by
        :return: [] of [] anything
            Matrix (ordered by drivers) of race results
        """

        data = Matrix(self.get_race_data(
            self.raw_year,
            self.raw_race,
            "result",
            ["Pos", "Pilote ", "Ch\\xc3\\xa2ssis ", "Tour ", "\xa0"]
        ))

    def get_qualification_summary(self, drivers=None):
        return self.get_race_data(
            self.raw_year,
            self.raw_race,
            "qualifications",
            ["Pos", "Pilote", "Ch\\xc3\\xa2ssis ", "Temps "]
        )

    def get_best_laps_summary(self, drivers=None):
        return self.get_race_data(
            self.raw_year,
            self.raw_race,
            "best_laps",
            ["Pos", "Pilote", "Ch\\xc3\\xa2ssis ", "n ", "Temps "]
        )

    @staticmethod
    def _get_race_completed(column, ratio=0.9):
        """
        :param column: [] of str
            List of laps completed
        :param ratio: float
            Laps must be over ratio * tot race laps iff completed
        :return: [] of bool
            Each row is True iff laps >= 90% race laps
        """

        column = [
            float(val)
            for val in column
        ]
        race_laps = max(column)
        completed_laps = ratio * race_laps

        return [
            val >= completed_laps
            for val in column
        ]

    @staticmethod
    def _get_race_vs_q(race_drivers, race_column, q_drivers, q_column):
        """
        :param race_drivers: [] of str
            List of drivers at the end of the race
        :param race_column: [] of str
            List of position of the drivers at the end of the race
        :param q_drivers: [] of str
            List of the drivers at the end of the qualifications
        :param q_column: [] of str
            List of position of the drivers at the end of the qualifications
        :return: [] of float
            Each row is driver.race_position - driver.q_position
        """

        race_vs_q = []

        for i, driver in enumerate(race_drivers):
            race_position = race_column[i]
            q_index = q_drivers.index(driver)
            q_position = q_column[q_index]

            race_vs_q.append(race_position - q_position)

        return race_vs_q

    @staticmethod
    def _get_best_lap_vs_q(bl_drivers, bl_column, q_drivers, q_column):
        """
        :param bl_drivers: [] of str
            List of drivers at the end of the race
        :param bl_column: [] of str
            List of position of the drivers at the end of the race
        :param q_drivers: [] of str
            List of the drivers at the end of the qualifications
        :param q_column: [] of str
            List of position of the drivers at the end of the qualifications
        :return: [] of float
            Each row is driver.race_position - driver.q_position
        """

        bl_vs_q = []

        for i, driver in enumerate(bl_drivers):
            bl_time = bl_column[i]  # raw data
            q_index = q_drivers.index(driver)
            q_time = q_column[q_index]

            bl_time = parse_time(pretty_time(bl_time))  # convert to nice format
            q_time = parse_time(pretty_time(q_time))
            bl_vs_q_time = 100.0 * (bl_time / q_time - 1.0)  # percentage

            bl_vs_q.append(bl_vs_q_time)

        return bl_vs_q

    def get_weekend_matrix(self):
        """
        :return: [] of [] of str
            Matrix of results of weekend
        """

        race = Matrix(self.get_race_summary())
        qualification = Matrix(self.get_qualification_summary())
        best_laps = Matrix(self.get_best_laps_summary())

        race_pos = race.get_column(0)
        driver = race.get_column(1)
        chassis = race.get_column(2)
        race_laps = race.get_column(3)
        race_completed = self._get_race_completed(race_laps)
        race_time = race.get_column(4)

        return summary

    def get_previous_years_results(self, n_years):
        year = int(self.raw_year)
        years = range(year - n_years + 1, year + 1)

        return self.RACE_SUMMARY_LABELS, {
            str(year):
                RaceExplorer(
                    self.raw_race, str(year), self.db_name
                ).get_weekend_matrix()[1]
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
            RaceExplorer(race, year, self.db_name).get_weekend_matrix()
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
    labels, summary = driver.get_weekend_matrix()
    print(pretty_format_table(labels, summary))
