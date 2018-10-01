#!/usr/bin/env python3
# coding: utf-8


""" Predicts race results based on db """

from scipy.stats import norm

from statsf1.tools.explorer import RaceExplorer

NUM_FORMAT = "{:.3f}"
GAUSS_PROB_MESSAGE = NUM_FORMAT + " +- " + NUM_FORMAT
RACE_COMPLETES_MESSAGE = "# past years = {}\n" \
                         "ratio of completes = " + GAUSS_PROB_MESSAGE + "\n" \
                                                                        "# drivers = {} =>\n" \
                                                                        "# completes = " + NUM_FORMAT + " +- " + NUM_FORMAT
RACE_COMPLETES_PROBS = [15.5, 16.5, 17.5]
RACE_COMPLETES_PROBS_MESSAGE = "\n".join([
    "P(< " + str(prob) + ") = " + NUM_FORMAT + "\n" \
                                               "P(> " + str(
        prob) + ") = " + NUM_FORMAT
    for prob in RACE_COMPLETES_PROBS
])


class Predictor:
    def __init__(self, race, year, db):
        self.explorer = RaceExplorer(race, year, db)

    def get_race_completes(self, n_drivers, n_years):
        labels, summaries = self.explorer.get_previous_years_result(n_years)
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
        mu, std = self.get_race_completes(n_drivers, n_years)
        mu = n_drivers * mu
        std = n_drivers * std
        gauss = norm(mu, std)

        probabilities = []
        for prob in RACE_COMPLETES_PROBS:
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

        print("--- normal distribution " + GAUSS_PROB_MESSAGE.format(mu, std))
        print(RACE_COMPLETES_PROBS_MESSAGE.format(*probabilities))

        print("--- probability VS stakes (more is better)")
        print(RACE_COMPLETES_PROBS_MESSAGE.format(*stakes))


def run(db):
    driver = Predictor("Japon", 2017, db)
    n_years = 7
    n_drivers = 20
    stakes = [2.25, 1.57, 1.72, 2, 1.28, 3.5]

    driver.print_race_completes(n_drivers, n_years, stakes)
