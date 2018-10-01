#!/usr/bin/env python3
# coding: utf-8


""" Core models for this bot """

import urllib.parse

from hal.internet.parser import HtmlTable
from hal.internet.web import Webpage
from hal.strings.utils import just_alphanum


class WebsiteObject:
    def __init__(self, text, url):
        self.text = text
        self.url = url
        self.web_page = Webpage(self.url)


class StatF1Scraper:
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
            text = url.loc.text
            title = text.split("/")[-1].replace(".aspx", "")
            self.years.append(Year(title, url))

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


class Year(WebsiteObject):
    def __init__(self, text, url):
        WebsiteObject.__init__(self, text, url)
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
            self.races.append(Race(title, url))

    def invalidate_cache(self):
        self.races = []


class Race(WebsiteObject):
    def __init__(self, text, url):
        WebsiteObject.__init__(self, text, url)

        self.race_entrants = None  # sections
        self.qualifications = None
        self.starting_grid = None
        self.result = None
        self.best_laps = None
        self.championship = None

    def _find_sections(self):
        self.web_page.get_html_source()

        links = self.web_page.soup \
            .find_all("div", {"class": "GPlink"})[0].find_all("a")

        self.race_entrants = TableSection(
            links[0].text,
            urllib.parse.urljoin(self.url, links[0].a["href"])
        )
        self.qualifications = TableSection(
            links[1].text,
            urllib.parse.urljoin(self.url, links[1].a["href"])
        )
        self.starting_grid = TableSection(
            links[2].text,
            urllib.parse.urljoin(self.url, links[2].a["href"])
        )
        self.result = TableSection(
            links[3].text,
            urllib.parse.urljoin(self.url, links[3].a["href"])
        )
        self.best_laps = TableSection(
            links[5].text,
            urllib.parse.urljoin(self.url, links[5].a["href"])
        )
        self.championship = TableSection(
            links[7].text,
            urllib.parse.urljoin(self.url, links[7].a["href"])
        )

    def parse(self):
        if not self.race_entrants:  # and so are None all the others ...
            self._find_sections()


class TableSection(WebsiteObject):
    def __init__(self, text, url):
        WebsiteObject.__init__(self, text, url)

        self.header = []
        self.rows = []

    def _find_data(self):
        self.web_page.get_html_source()
        table = self.web_page.soup.find_all("table")[0]
        table = HtmlTable(str(table))
        data = table.parse()

        self.header = data[0]
        self.rows = data[1:]

    def parse(self):
        if not self.header:
            self.parse()
