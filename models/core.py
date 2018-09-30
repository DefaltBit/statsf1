#!/usr/bin/env python3
# coding: utf-8


""" Core models for this bot """


class WebsiteObject:
    def __init__(self, text, url):
        self.text = text
        self.url = url


class Year(WebsiteObject):
    def __init__(self, text, url):
        WebsiteObject.__init__(self, text, url)
        self.races = None

    def get_all_races(self):
        if self.races is None:
            self._find_all_races()

        return self.races

    def _find_all_races(self):
        self.races = []  # todo


class Race(WebsiteObject):
    def __init__(self, text, url):
        WebsiteObject.__init__(self, text, url)
        # todo

    def parse(self):
        return {}  # todo


class WebsiteAnalyzer:
    def __init__(self, root):
        self.root_url = root
        self.years = None

    def get_all_years(self):
        if self.years is None:
            self._find_all_years()

        return self.years

    def _find_all_years(self):
        self.years = []  # todo

    def get_all_races(self, year):
        return year.get_all_races()
