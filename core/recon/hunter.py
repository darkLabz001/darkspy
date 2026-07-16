#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
from core.lib import http
from core.lib import printer

class hunter_check:
    con = http.http()
    printf = printer.printer()

    def __init__(self, domain):
        self.domain = domain
        self.emails = []

    def search(self):
        self.printf.test("Checking Hunter.io for \"%s\"..." % self.domain)
        try:
            url = "https://hunter.io/search/%s" % self.domain
            resp = self.con.get(url, timeout=15)
            if resp and 'email' in resp.lower():
                import re
                pattern = r'[a-zA-Z0-9._%+-]+@' + re.escape(self.domain)
                found = re.findall(pattern, resp, re.IGNORECASE)
                for e in found:
                    if e not in self.emails:
                        self.emails.append(e)
                if self.emails:
                    self.printf.plus("Found %d emails on Hunter.io" % len(self.emails))
                else:
                    self.printf.error("No emails found on Hunter.io")
            else:
                self.printf.error("Hunter.io returned no useful data")
        except Exception as e:
            self.printf.error("Hunter.io error: %s" % str(e))

    def getemail(self):
        return self.emails

    def process(self):
        self.search()
