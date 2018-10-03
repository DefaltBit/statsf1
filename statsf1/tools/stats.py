#!/usr/bin/env python3
# coding: utf-8


""" Gets stats about results in db """

from hal.data.lists import find_commons
from hal.streams.pretty_table import pretty_format_table
from scipy.stats import norm

from statsf1.data import NUM_FORMAT, DNF, NORM_PROB_FORMAT, SOL, LOW_NUM_FORMAT, \
    TOL, DNF_POS_VALUE
from statsf1.tools.explorer import RaceExplorer, Explorer
from statsf1.tools.utils import parse_time

# formatting
COMPLETES_FORMAT = "# past years = {}\n" \
                   "ratio of completes = " + NORM_PROB_FORMAT + "\n" \
                                                                "# drivers = {} =>\n" \
                                                                "# completes = " + NUM_FORMAT + " +- " + NUM_FORMAT
PROB_FORMAT = "P({}) = " + NUM_FORMAT
NORM_DISTRIBUTION_FORMAT = SOL + "normal distribution " + NORM_PROB_FORMAT
RACE_SUMMARY_FORMAT = SOL + "summary of {} in {}"
DRIVER_SUMMARY_FORMAT = SOL + "summary of {} at {} from {} to {}"
COMPLETES_MESSAGE = SOL + "who complets? Everyone, except the following:"

# probability messages
PROB_VS_STAKE_MESSAGE = SOL + "probability VS stakes (more is better)"
LT_PROB_FORMAT = "P(< " + LOW_NUM_FORMAT + ") = " + NUM_FORMAT
IN_BETWEEN_PROB_FORMAT = "P(" + LOW_NUM_FORMAT + " < " + LOW_NUM_FORMAT + \
                         ") = " + NUM_FORMAT
GT_PROB_FORMAT = "P(> " + LOW_NUM_FORMAT + ") = " + NUM_FORMAT

# probabilities
COMPLETES_PROBS = [15.5, 16.5, 17.5]
WIN_QUALIFY_PROBS = [0.1, 0.2, 0.2]
WIN_RACE_PROBS = [3, 6, 6]
WIN_Q_PROBS = ["1", "2", "3-4", "5-7", "8-13", "14-20"]

# stakes data (bet365 -> Formula 1)
STAKES = {
    "completes": [1.57, 2.25, 2, 1.72, 3.5, 1.28],
    "q_margin": [2.62, 3, 2.5],
    "race_margin": [3.25, 3.5, 1.9],
    "win_q_pos": [1.62, 3.75, 6.5, 17, 34, 51]
}


def print_probabilities(stakes, probabilities, messages):
    most_probable = max(probabilities)
    lists = zip(stakes, probabilities, messages)
    for i, (stake, prob, message) in enumerate(lists):
        try:
            msg = message.format(stake, prob)
        except:
            msg = message.format(stakes[i - 1], stake, prob)

        msg = "{:>21}".format(msg)

        if prob == most_probable:
            msg += " <-- best"

        print(msg)


def print_probabilities_summary(title, labels, probabilities, stakes, messages):
    print(title)
    print_probabilities(
        labels,
        probabilities,
        messages
    )

    print(PROB_VS_STAKE_MESSAGE)
    print_probabilities(
        labels,
        stakes,
        messages
    )


def get_probabilities(stakes):
    return [
        1.0 / stake
        for stake in stakes
    ]  # calculate probability of each stake


def compare_to_stakes(probabilities, stakes):
    return [
        prob / stake * prob
        for prob, stake in zip(probabilities, stakes)
    ]  # compare predicted probability with staked one


class Statistician:
    def __init__(self, race, year, db, n_years):
        self.explorer = RaceExplorer(race, year, db)
        self.n_years = n_years

    def _get_years(self, including_this_year):
        max_year = int(self.explorer.raw_year)
        if including_this_year:
            max_year += 1

        min_year = max_year - self.n_years - 1
        return range(min_year, max_year)

    def get_matrix(self, data_label, col_index=0, driver=None, chassis=None,
                   including_this_year=True):
        years = self._get_years(including_this_year)
        results = {
            str(year):
                self.explorer.get_results_of_label_on(
                    data_label, str(year), driver=driver, chassis=chassis
                )
            for year in years
        }  # all races results across all years

        races = find_commons([
            list(results.keys())  # result keys are the name of the races
            for year, results in results.items()
        ]) + [self.explorer.raw_race]  # races in common between years

        results = {
            year: {
                race: data
                for race, data in results.items() if race in races
            }
            for year, results in results.items()
        }  # filter by race

        row_labels = sorted(results.keys())
        column_labels = sorted(results[row_labels[0]].keys())
        row_labels = list(reversed(row_labels))  # from last year to oldest
        table = [
            [
                results[year][race][col_index] if race in races else DNF
                for race in column_labels  # get just winner
            ]
            for year in row_labels
        ]

        races_to_remove = [
            i
            for i, col in enumerate(column_labels)
            if (table[0][i] == DNF and col != self.explorer.raw_race)
        ]  # remove races that are not in all years
        table = [
            [
                col
                for i, col in enumerate(row)
                if i not in races_to_remove
            ]
            for row in table
        ]
        column_labels = [
            label
            for i, label in enumerate(column_labels)
            if i not in races_to_remove
        ]

        for i, row in enumerate(table):  # fix DNF data
            for j, col in enumerate(row):
                if col == DNF:
                    table[i][j] = DNF_POS_VALUE

        return row_labels, column_labels, table

    def get_race_matrix(self, data_label, col_index=0, driver=None,
                        chassis=None, including_this_year=True):
        row_labels, column_labels, table = self.get_matrix(
            data_label, col_index=col_index, driver=driver,
            chassis=chassis, including_this_year=including_this_year
        )

        race_index = column_labels.index(self.explorer.raw_race)
        column = [
            row[race_index]
            for row in table
        ]
        return row_labels, column

    def get_winners_matrix(self, label):
        return self.get_matrix(label, col_index=0)

    def _get_race_completes(self):
        _, summaries = self.explorer.get_previous_years_results(self.n_years)
        summary = {
            year: float(len([
                row[4]
                for row in data
                if row[4] == "yes"
            ])) / len(data)  # ratio
            for year, data in summaries.items()
        }
        x = [
            count for year, count in summary.items()
        ]

        return norm.fit(x)

    def print_race_completes(self, n_drivers, stakes):
        mu, std = self._get_race_completes()
        mu = n_drivers * mu
        std = n_drivers * std
        gauss = norm(mu, std)

        probabilities = []
        for prob in COMPLETES_PROBS:
            probabilities.append(1.0 - gauss.cdf(prob + 0.5))  # discreet
            probabilities.append(gauss.cdf(prob - 0.5))

        stakes = get_probabilities(stakes)
        stakes = compare_to_stakes(probabilities, stakes)

        print_probabilities_summary(
            NORM_DISTRIBUTION_FORMAT.format(mu, std),
            sum([2 * [x] for x in COMPLETES_PROBS], []),
            probabilities,
            stakes,
            [GT_PROB_FORMAT, LT_PROB_FORMAT] * len(COMPLETES_PROBS)
        )

    def _get_driver_completes(self):
        _, summaries = self.explorer.get_previous_years_results(self.n_years)
        summary = {}

        for _, summ in summaries.items():
            drivers = [
                row[1] for row in summ
            ]
            completed = [
                row[4] for row in summ
            ]

            for driver, has_completed in zip(drivers, completed):
                if driver not in summary:
                    summary[driver] = {
                        "count": 0.0,
                        "completed": 0.0
                    }

                if has_completed == "yes":
                    summary[driver]["completed"] += 1

                summary[driver]["count"] += 1

        return {
            driver: data["completed"] / data["count"]  # ratio
            for driver, data in summary.items()
        }

    def print_driver_completes(self):
        summary = self._get_driver_completes()
        summary = sorted(summary.items(),
                         key=lambda x: x[0].split(" ")[-1])  # surname

        print(COMPLETES_MESSAGE)
        for driver, prob in summary:
            if prob < 1:
                msg = PROB_FORMAT.format(driver, prob)
                print("{:>30}".format(msg))

    def _get_qualify_margin(self):
        _, summaries = self.explorer.get_previous_years_results(self.n_years)
        summary = {
            year: parse_time(data[1][7]) - parse_time(data[0][7])
            for year, data in summaries.items()
        }
        x = [
            diff for year, diff in summary.items()
        ]

        return norm.fit(x)

    def print_qualify_margin(self, stakes):
        mu, std = self._get_qualify_margin()
        gauss = norm(mu, std)

        probabilities = [
            gauss.cdf(WIN_QUALIFY_PROBS[0]),
            gauss.cdf(WIN_QUALIFY_PROBS[1]) - gauss.cdf(WIN_QUALIFY_PROBS[0]),
            1.0 - gauss.cdf(WIN_QUALIFY_PROBS[1])
        ]

        stakes = get_probabilities(stakes)
        stakes = compare_to_stakes(probabilities, stakes)

        print_probabilities_summary(
            NORM_DISTRIBUTION_FORMAT.format(mu, std),
            WIN_QUALIFY_PROBS,
            probabilities,
            stakes,
            [LT_PROB_FORMAT, IN_BETWEEN_PROB_FORMAT, GT_PROB_FORMAT]
        )

    def _get_race_margin(self):
        _, summaries = self.explorer.get_previous_years_results(self.n_years)
        summary = {
            year: parse_time(data[1][5]) - parse_time(data[0][5])
            for year, data in summaries.items()
        }
        x = [
            diff for year, diff in summary.items()
        ]

        return norm.fit(x)

    def print_race_margin(self, stakes):
        mu, std = self._get_race_margin()
        gauss = norm(mu, std)

        probabilities = [
            gauss.cdf(WIN_RACE_PROBS[0]),
            gauss.cdf(WIN_RACE_PROBS[1]) - gauss.cdf(WIN_RACE_PROBS[0]),
            1.0 - gauss.cdf(WIN_RACE_PROBS[1])
        ]

        stakes = get_probabilities(stakes)
        stakes = compare_to_stakes(probabilities, stakes)

        print_probabilities_summary(
            NORM_DISTRIBUTION_FORMAT.format(mu, std),
            WIN_RACE_PROBS,
            probabilities,
            stakes,
            [LT_PROB_FORMAT, IN_BETWEEN_PROB_FORMAT, GT_PROB_FORMAT]
        )

    def _get_winner_q_position(self):
        _, summaries = self.explorer.get_previous_years_results(self.n_years)
        summary = {
            year: float(data[0][6])  # position of winner in qualifications
            for year, data in summaries.items()
        }
        x = [
            pos for year, pos in summary.items()
        ]

        return norm.fit(x)

    def print_winner_q_position(self, n_drivers, stakes):
        mu, std = self._get_winner_q_position()
        gauss = norm(mu, std)

        raw_probs = [
            gauss.cdf(pos + 0.5) - gauss.cdf(pos - 0.5)  # discreet
            for pos in range(1, n_drivers + 1)
        ]

        probabilities = []  # calculate prob for given stakes
        for stake in WIN_Q_PROBS:
            if "-" in stake:
                max_pos = int(stake.split("-")[-1])
                min_pos = int(stake.split("-")[0])
                prob = sum(
                    raw_probs[i]
                    for i in range(min_pos - 1, max_pos)
                )
            else:
                pos = int(stake)
                prob = raw_probs[pos - 1]

            probabilities.append(prob)

        stakes = get_probabilities(stakes)
        stakes = compare_to_stakes(probabilities, stakes)

        print_probabilities_summary(
            NORM_DISTRIBUTION_FORMAT.format(mu, std),
            WIN_Q_PROBS,
            probabilities,
            stakes,
            [PROB_FORMAT] * n_drivers
        )

    def print_summary(self):
        labels, summary = self.explorer.get_summary()
        print(RACE_SUMMARY_FORMAT.format(
            self.explorer.raw_race, self.explorer.raw_year
        ))
        print(pretty_format_table(labels, summary[:10]))

    def print_driver_summary(self, driver):
        labels, summary = \
            self.explorer.get_previous_years_matrix(self.n_years, driver)
        first_year = summary[-1][0]
        last_year = summary[0][0]

        print(DRIVER_SUMMARY_FORMAT.format(
            driver, self.explorer.raw_race, first_year, last_year
        ))
        print(pretty_format_table(labels, summary))

    def get_chassis(self, including_this_year=True):
        years = self._get_years(including_this_year)
        chassis = [
            Explorer(
                self.explorer.db_name
            ).get_chassis(str(year))
            for year in years
        ]
        return find_commons(chassis)  # chassis common in all races

    def get_drivers(self, including_this_year=True):
        years = self._get_years(including_this_year)
        drivers = [
            Explorer(
                self.explorer.db_name
            ).get_driver(str(year))
            for year in years
        ]
        return find_commons(drivers)  # chassis common in all races


def run(race, driver, year, n_years, n_drivers, db):
    stats = Statistician(race, year, db, n_years)

    print(TOL + "# drivers who complete the race")
    stats.print_race_completes(n_drivers, STAKES["completes"])

    print(TOL + "Drivers who complete the race")
    stats.print_driver_completes()

    print(TOL + "Q time win margin")
    stats.print_qualify_margin(STAKES["q_margin"])

    print(TOL + "Race time win margin")
    stats.print_race_margin(STAKES["race_margin"])

    print(TOL + "Q position of winner")
    stats.print_winner_q_position(n_drivers, STAKES["win_q_pos"])

    print(TOL + "Race summary")
    stats.print_summary()

    print(TOL + "Driver summary")
    stats.print_driver_summary(driver)