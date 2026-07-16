#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
from core.lib import http
from core.lib import printer

class crtsh:
    con = http.http()
    printf = printer.printer()

    def __init__(self, target):
        self.target = target
        self.emails = []

    def search(self):
        self.printf.test("Searching certificate transparency logs for \"%s\"..." % self.target)
        try:
            url = "https://crt.sh/?q=.%s&output=json" % self.target
            resp = self.con.get(url, timeout=20)
            if not resp or '<html' in resp[:200].lower():
                self.printf.error("crt.sh is unavailable (try again later)")
                return
            data = json.loads(resp)
            for entry in data:
                name = entry.get('name_value', '')
                for line in name.split('\n'):
                    line = line.strip().lower()
                    if '@' in line and self.target in line:
                        if line not in self.emails:
                            self.emails.append(line)
            if self.emails:
                self.printf.plus("Found %d emails from certificate logs" % len(self.emails))
            else:
                self.printf.error("No emails found in certificate logs")
        except json.JSONDecodeError:
            self.printf.error("Invalid response from crt.sh")
        except Exception as e:
            self.printf.error("crt.sh error: %s" % str(e))

    def getemail(self):
        return self.emails

    def process(self):
        self.search()
