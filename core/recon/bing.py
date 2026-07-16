#!/usr/bin/python3
# -*- coding: utf-8 -*-

from core.lib import parser
from core.lib import http

class bing:
    def __init__(self, target):
        self.target = target
        self.results = ""

    def search(self):
        con = http.http()
        queries = [
            '"@%s"' % self.target,
            '"@%s" contact' % self.target,
            '"@%s" email' % self.target,
            'site:linkedin.com "@%s"' % self.target,
            'site:facebook.com "@%s"' % self.target,
        ]
        for q in queries:
            try:
                url = "https://www.bing.com/search?q=" + q.replace(' ', '+') + "&count=50"
                resp = con.get(url)
                if resp:
                    self.results += resp
            except Exception:
                pass

    def getemail(self):
        email = parser.parser(self.results, self.target)
        return email.email()

    def process(self):
        self.search()
