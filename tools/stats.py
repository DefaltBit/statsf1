#!/usr/bin/env python3
# coding: utf-8


""" Predicts race results based on db """

from scipy.stats import norm

from statsf1.tools.explorer import RaceExplorer

NUM_FORMAT = "{:.3f}"
NORM_PROB_FORMAT = NUM_FORMAT + " +- " + NUM_FORMAT
COMPLETES_FORMAT = "# past years = {}\n" \
                   "ratio of completes = " + NORM_PROB_FORMAT + "\n" \
                                                                "# drivers = {} =>\n" \
                                                                "# completes = " + NUM_FORMAT + " +- " + NUM_FORMAT
COMPLETES_PROBS = [15.5, 16.5, 17.5]
DRIVER_COMPLETES_FORMAT = "{:>21}) = {:.3f}"
PROB_MESSAGE = "P(< {}) = " + NUM_FORMAT


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
            msg = PROB_MESSAGE.format(stake_prob, prob)
            if prob == max(probabilities):
                msg += " <-- most probable"
            print(msg)

        print("--- probability VS stakes (more is better)")
        for i, stake in enumerate(stakes):
            stake_prob = COMPLETES_PROBS[int(i / 2)]
            msg = PROB_MESSAGE.format(stake_prob, stake)
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
                print(DRIVER_COMPLETES_FORMAT.format("P(" + driver, prob))

    def _get_qualify_margin(self, n_years):
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


def run(db):
    driver = Statistician("Japon", 2017, db)
    n_years = 7
    n_drivers = 20
    stakes = [2.25, 1.57, 1.72, 2, 1.28, 3.5]

    # driver.print_race_completes(n_drivers, n_years, stakes)
    driver.print_driver_completes(n_years)
