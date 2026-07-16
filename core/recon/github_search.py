#!/usr/bin/python3
# -*- coding: utf-8 -*-

from core.lib import http
from core.lib import parser
from core.lib import printer
import re

class github:
    con = http.http()
    printf = printer.printer()

    def __init__(self, target):
        self.target = target
        self.results = ""
        self.emails = []

    def search(self):
        self.printf.test("Searching GitHub for \"%s\" emails..." % self.target)
        queries = [
            '"@%s"' % self.target,
            '"@%s" password' % self.target,
            '"@%s" key' % self.target,
        ]
        for q in queries:
            try:
                url = "https://github.com/search?q=" + q.replace(' ', '+') + "&type=code"
                resp = self.con.get(url)
                if resp:
                    self.results += resp
            except Exception:
                pass

        p = parser.parser(self.results, self.target)
        found = p.email_from_text()
        for e in found:
            if e not in self.emails:
                self.emails.append(e)

        if self.emails:
            self.printf.plus("Found %d emails on GitHub" % len(self.emails))
        else:
            self.printf.error("No emails found on GitHub")

    def getemail(self):
        return self.emails

    def process(self):
        self.search()
