#!/usr/bin/env python3
# coding: utf-8


""" Core models for this bot """

import urllib.parse

from hal.internet.parser import HtmlTable
from hal.internet.web import Webpage
from hal.strings.utils import just_alphanum

from statsf1.tools.logger import log_year, log_race, log_error


class WebsiteObject:
    def __init__(self, text, url):
        self.text = text
        self.url = url
        self.web_page = Webpage(self.url)

        self.select_lang()

    def select_lang(self, preferred="en"):
        lang = "/" + preferred + "/"
        self.url = self.url.replace("/fr/", lang)


class StatF1:
    YEARS_SITEMAP = "sitemapsaison.xml"

    def __init__(self, root_url="http://statsf1.com/"):
        self.root = root_url
        self.years = []
        self.years_sitemap = urllib.parse.urljoin(self.root, self.YEARS_SITEMAP)

    def get_all_years(self):
        if not self.years:
            self._find_all_years()

        return self.years

    def _find_all_years(self):
        self.years = []  # reset
        web_page = Webpage(self.years_sitemap)
        web_page.get_html_source()  # download

        for url in web_page.soup.find_all("url"):
            url = url.find("loc").text
            title = url.split("/")[-1].replace(".aspx", "")

            self.years.append(Year(title, url))
            log_year(title)

    def get_races(self, year):
        for y in self.get_all_years():
            if y.text == str(year):
                return y.get_all_races()

    def get_all_races(self):
        races = []

        for year in self.get_all_years():
            races += year.get_all_races()

        return races

    def invalidate_cache(self):
        self.years = []

    def get_year(self, year):
        for y in self.get_all_years():
            if y.text == year:
                return y

        return None


class Year(WebsiteObject):
    def __init__(self, text, url):
        super().__init__(text, url)
        self.races = []

    def get_all_races(self):
        if not self.races:
            self._find_all_races()

        return self.races

    def _find_all_races(self):
        self.races = []  # reset
        self.web_page.get_html_source()

        for div in self.web_page.soup.find_all("div", {"class": "gp"}):
            url = div.find_all("div")[1].a["href"]  # relative url
            url = urllib.parse.urljoin(self.url, url)  # full url

            title = just_alphanum(div.find("div").text)
            title = " ".join(title.split(" ")[1:])  # remove number

            race = Race(title, url)
            self.races.append(race)
            log_race(race)

    def invalidate_cache(self):
        self.races = []

    def to_dict(self):
        out = {}

        for race in self.races:
            out[race.text] = race.to_dict()

        return out


class Race(WebsiteObject):
    def __init__(self, text, url):
        super().__init__(text, url)

        self.year = self.url.split("/")[4]  # race's year
        self.race_entrants = None  # sections
        self.qualifications = None
        self.result = None
        self.best_laps = None

    def _find_sections(self):
        self.web_page.get_html_source()

        links = self.web_page.soup.find_all("div", {"class": "GPlink"})[0]
        links = links.find_all("a")

        self.race_entrants = TableSection(
            links[0].text,  # relative url
            urllib.parse.urljoin(self.url, links[0]["href"])
        )
        self.qualifications = TableSection(
            links[1].text,  # relative url
            urllib.parse.urljoin(self.url, links[1]["href"])
        )
        self.result = TableSection(
            links[3].text,  # relative url
            urllib.parse.urljoin(self.url, links[3]["href"])
        )
        self.best_laps = TableSection(
            links[5].text,  # relative url
            urllib.parse.urljoin(self.url, links[5]["href"])
        )

    def parse(self):
        try:
            if not self.race_entrants:  # and so are None all the others ...
                self._find_sections()

            self.race_entrants.parse()
            self.qualifications.parse()
            self.result.parse()
            self.best_laps.parse()
        except:  # race is in the future
            log_error(self, cause="incorrect parsing")

    def to_dict(self):
        out = {
            "year": int(self.year),
            "name": str(self.text),
            "url": str(self.url)
        }

        try:
            out["race_entrants"] = self.race_entrants.to_dict()
            out["qualifications"] = self.qualifications.to_dict()
            out["result"] = self.result.to_dict()
            out["best_laps"] = self.best_laps.to_dict()
        except:  # race is in the future
            log_error(self, cause="incorrect dict conversion")

        return out


class TableSection(WebsiteObject):
    def __init__(self, text, url):
        super().__init__(text, url)

        self.labels = []
        self.rows = []

    def _find_data(self):
        self.web_page.get_html_source()
        table = self.web_page.soup.find("table")

        if table is None:  # no table found
            self.labels = []
            self.rows = []
        else:
            table = HtmlTable(str(table))
            data = table.parse()

            self.labels = data[0]
            self.rows = data[1:]

        self._fix_data()

    def _fix_data(self):
        if len(self.labels) == 6 and len(self.rows[0]) == 8:  # standings
            self.rows = [
                [row[0], row[1], row[2], row[3], row[5], row[7]]
                for row in self.rows
            ]

    def parse(self):
        if not self.labels:
            self._find_data()

    def to_dict(self):
        out = {}

        for i, label in enumerate(self.labels):
            column = [
                row[i]
                for row in self.rows
            ]
            out[label] = column

        return out
