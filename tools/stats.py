#!/usr/bin/env python3
# coding: utf-8


""" Predicts race results based on db """
from hal.streams.pretty_table import pretty_format_table
from scipy.stats import norm

from statsf1.tools.explorer import RaceExplorer
from statsf1.tools.utils import parse_time, NUM_FORMAT

LOW_NUM_FORMAT = "{:.1f}"
NORM_PROB_FORMAT = NUM_FORMAT + " +- " + NUM_FORMAT
COMPLETES_FORMAT = "# past years = {}\n" \
                   "ratio of completes = " + NORM_PROB_FORMAT + "\n" \
                                                                "# drivers = {} =>\n" \
                                                                "# completes = " + NUM_FORMAT + " +- " + NUM_FORMAT
COMPLETES_PROBS = [15.5, 16.5, 17.5]
WIN_QUALIFY_PROBS = [0.1, 0.2, 0.2]
WIN_RACE_PROBS = [3, 6, 6]
DRIVER_COMPLETES_FORMAT = "P({}) = " + NUM_FORMAT
LT_PROB_MESSAGE = "P(< " + LOW_NUM_FORMAT + ") = " + NUM_FORMAT
IN_BETWEEN_PROB_MESSAGE = "P(" + LOW_NUM_FORMAT + " < " + LOW_NUM_FORMAT + ") = " + NUM_FORMAT
GT_PROB_MESSAGE = "P(> " + LOW_NUM_FORMAT + ") = " + NUM_FORMAT


def print_probabilities(stakes, probabilities, messages):
    most_probable = max(probabilities)
    lists = zip(stakes, probabilities, messages)
    for i, (stake, prob, message) in enumerate(lists):
        try:
            msg = message.format(stake, prob)
        except:
            msg = message.format(stakes[i - 1], stake, prob)

        msg = "{:>20}".format(msg)

        if prob == most_probable:
            msg += " <-- best"

        print(msg)


class Statistician:
    def __init__(self, race, year, db):
        self.explorer = RaceExplorer(race, year, db)

    def _get_race_completes(self, n_years):
        _, summaries = self.explorer.get_previous_years_result(n_years)
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

    def print_race_completes(self, n_drivers, n_years, stakes):
        mu, std = self._get_race_completes(n_years)
        mu = n_drivers * mu
        std = n_drivers * std
        gauss = norm(mu, std)

        probabilities = []
        for prob in COMPLETES_PROBS:
            probabilities.append(gauss.cdf(prob - 0.5))  # discreet
            probabilities.append(1.0 - gauss.cdf(prob + 0.5))

        stakes = [
            1.0 / stake
            for stake in stakes
        ]  # calculate probability of each stake
        stakes = [
            prob / stake * prob
            for prob, stake in zip(probabilities, stakes)
        ]  # compare predicted probability with staked one

        print("--- normal distribution " + NORM_PROB_FORMAT.format(mu, std))
        for i, prob in enumerate(probabilities):
            stake_prob = COMPLETES_PROBS[int(i / 2)]
            msg = LT_PROB_MESSAGE.format(stake_prob, prob)
            if prob == max(probabilities):
                msg += " <-- most probable"
            print(msg)

        print("--- probability VS stakes (more is better)")
        for i, stake in enumerate(stakes):
            stake_prob = COMPLETES_PROBS[int(i / 2)]
            msg = LT_PROB_MESSAGE.format(stake_prob, stake)
            if stake == max(stakes):
                msg += " <-- best choice"
            print(msg)

    def _get_driver_completes(self, n_years):
        _, summaries = self.explorer.get_previous_years_result(n_years)
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

    def print_driver_completes(self, n_years):
        summary = self._get_driver_completes(n_years)
        summary = sorted(summary.items(),
                         key=lambda x: x[0].split(" ")[-1])  # surname

        print("--- who complets? Everyone, except the following:")
        for driver, prob in summary:
            if prob < 1:
                msg = DRIVER_COMPLETES_FORMAT.format(driver, prob)
                print("{:>30}".format(msg))

    def _get_qualify_margin(self, n_years):
        _, summaries = self.explorer.get_previous_years_result(n_years)
        summary = {
            year: parse_time(data[1][7]) - parse_time(data[0][7])
            for year, data in summaries.items()
        }
        x = [
            diff for year, diff in summary.items()
        ]

        return norm.fit(x)

    def print_qualify_margin(self, n_years, stakes):
        mu, std = self._get_qualify_margin(n_years)
        gauss = norm(mu, std)

        probabilities = [
            gauss.cdf(WIN_QUALIFY_PROBS[0]),
            gauss.cdf(WIN_QUALIFY_PROBS[1]) - gauss.cdf(WIN_QUALIFY_PROBS[0]),
            1.0 - gauss.cdf(WIN_QUALIFY_PROBS[1])
        ]

        stakes = [
            1.0 / stake
            for stake in stakes
        ]  # calculate probability of each stake
        stakes = [
            prob / stake * prob
            for prob, stake in zip(probabilities, stakes)
        ]  # compare predicted probability with staked one

        print("--- normal distribution " + NORM_PROB_FORMAT.format(mu, std))
        print_probabilities(
            WIN_QUALIFY_PROBS,
            probabilities,
            [LT_PROB_MESSAGE, IN_BETWEEN_PROB_MESSAGE, GT_PROB_MESSAGE]
        )

        print("--- probability VS stakes (more is better)")
        print_probabilities(
            WIN_QUALIFY_PROBS,
            stakes,
            [LT_PROB_MESSAGE, IN_BETWEEN_PROB_MESSAGE, GT_PROB_MESSAGE]
        )

    def _get_race_margin(self, n_years):
        _, summaries = self.explorer.get_previous_years_result(n_years)
        summary = {
            year: parse_time(data[1][5]) - parse_time(data[0][5])
            for year, data in summaries.items()
        }
        x = [
            diff for year, diff in summary.items()
        ]

        return norm.fit(x)

    def print_race_margin(self, n_years, stakes):
        mu, std = self._get_race_margin(n_years)
        gauss = norm(mu, std)

        probabilities = [
            gauss.cdf(WIN_RACE_PROBS[0]),
            gauss.cdf(WIN_RACE_PROBS[1]) - gauss.cdf(WIN_RACE_PROBS[0]),
            1.0 - gauss.cdf(WIN_RACE_PROBS[1])
        ]

        stakes = [
            1.0 / stake
            for stake in stakes
        ]  # calculate probability of each stake
        stakes = [
            prob / stake * prob
            for prob, stake in zip(probabilities, stakes)
        ]  # compare predicted probability with staked one

        print("--- normal distribution " + NORM_PROB_FORMAT.format(mu, std))
        print_probabilities(
            WIN_RACE_PROBS,
            probabilities,
            [LT_PROB_MESSAGE, IN_BETWEEN_PROB_MESSAGE, GT_PROB_MESSAGE]
        )

        print("--- probability VS stakes (more is better)")
        print_probabilities(
            WIN_RACE_PROBS,
            stakes,
            [LT_PROB_MESSAGE, IN_BETWEEN_PROB_MESSAGE, GT_PROB_MESSAGE]
        )


def run(db):
    race = "Japon"
    year = 2017
    n_years = 2
    n_drivers = 20
    completes_stakes = [2.25, 1.57, 1.72, 2, 1.28, 3.5]
    qualify_margin_stakes = [2.62, 3, 2.5]
    race_margin_stakes = [3.25, 3.5, 1.9]

    driver = Statistician(race, year, db)
    # driver.print_race_completes(n_drivers, n_years, completes_stakes)
    # driver.print_driver_completes(n_years)
    # driver.print_qualify_margin(n_years, qualify_margin_stakes)
    driver.print_race_margin(n_years, race_margin_stakes)

    labels, summary = driver.explorer.get_summary()
    print("--- summary for " + race + " in " + str(year))
    print(pretty_format_table(labels, summary[:10]))
