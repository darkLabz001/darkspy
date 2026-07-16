#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import hashlib
from core.lib import http
from core.lib import printer

class breach_check:
    printf = printer.printer()

    def __init__(self, email):
        self.email = email.lower().strip()
        self.breaches = []

    def check_dehashed_light(self):
        self.printf.test("Checking breach databases...")
        try:
            con = http.http()
            url = "https://check.haveibeenpwned.com/api/v3/breachedaccount/%s?truncateResponse=false" % self.email
            resp = con.get(url, timeout=10)
            if resp and resp.status_code == 200:
                data = json.loads(resp)
                for b in data:
                    name = b.get('Name', 'Unknown')
                    date = b.get('BreachDate', 'Unknown')
                    count = b.get('PwnCount', 0)
                    self.printf.plus("Breach: %s (%s) - %s records" % (name, date, count))
                    self.breaches.append({'name': name, 'date': date, 'count': count})
            elif resp and resp.status_code == 404:
                self.printf.plus("No breaches found (clean!)")
            else:
                self.printf.error("HIBP API requires API key, trying alternative...")
        except Exception:
            self.printf.error("HIBP lookup failed")

    def check_leakcheck(self):
        self.printf.test("Checking LeakCheck (free tier)...")
        try:
            con = http.http()
            username = self.email.split('@')[0]
            domain = self.email.split('@')[1]
            url = "https://leakcheck.io/api/public?check=%s" % username
            resp = con.get(url, timeout=10)
            if resp and '"found"' in resp:
                data = json.loads(resp)
                found = data.get('found', 0)
                if found > 0:
                    self.printf.plus("Found in %s leak(s)" % found)
                    sources = data.get('sources', [])
                    for s in sources[:5]:
                        self.printf.plus("  Source: %s" % s.get('name', 'Unknown'))
                else:
                    self.printf.plus("No leaks found")
            else:
                self.printf.error("LeakCheck returned no data")
        except Exception:
            self.printf.error("LeakCheck lookup failed")

    def check_emailrep(self):
        self.printf.test("Checking EmailRep.io...")
        try:
            con = http.http()
            url = "https://emailrep.io/%s" % self.email
            resp = con.get(url, timeout=10)
            if resp:
                data = json.loads(resp)
                reputation = data.get('reputation', 'unknown')
                suspicious = data.get('suspicious', False)
                details = data.get('details', {})
                deliverable = details.get('deliverable', None)
                malicious = details.get('malicious_activity', False)
                credentials_leaked = details.get('credentials_leaked', False)
                data_breach = details.get('data_breach', False)
                first_seen = details.get('first_seen', 'Unknown')
                last_seen = details.get('last_seen', 'Unknown')
                spam = details.get('spam', False)

                self.printf.plus("Reputation: %s" % reputation)
                self.printf.plus("Suspicious: %s" % suspicious)
                self.printf.plus("Deliverable: %s" % deliverable)
                self.printf.plus("Credentials leaked: %s" % credentials_leaked)
                self.printf.plus("Data breach: %s" % data_breach)
                self.printf.plus("Malicious activity: %s" % malicious)
                self.printf.plus("Spam: %s" % spam)
                self.printf.plus("First seen: %s" % first_seen)
                self.printf.plus("Last seen: %s" % last_seen)
                self.breaches.append({
                    'source': 'emailrep',
                    'reputation': reputation,
                    'suspicious': suspicious,
                    'credentials_leaked': credentials_leaked,
                    'data_breach': data_breach,
                })
            else:
                self.printf.error("EmailRep returned no data")
        except Exception:
            self.printf.error("EmailRep lookup failed")

    def check_holehe(self):
        self.printf.test("Checking holehe (email existence)...")
        try:
            con = http.http()
            sites = [
                ('https://api.twitter.com/i/users/email_available.json?email=%s', 'Twitter'),
                ('https://www.instagram.com/accounts/web/login/?email=%s', 'Instagram'),
            ]
            for url_template, name in sites:
                try:
                    url = url_template % self.email
                    resp = con.get(url, timeout=8)
                    if resp:
                        data = json.loads(resp) if resp.startswith('{') or resp.startswith('[') else {}
                        if isinstance(data, dict) and data.get('taken', False):
                            self.printf.plus("Registered on %s" % name)
                            self.breaches.append({'source': name.lower(), 'registered': True})
                        elif isinstance(data, dict) and 'available' in data:
                            if not data.get('available', True):
                                self.printf.plus("Registered on %s" % name)
                                self.breaches.append({'source': name.lower(), 'registered': True})
                except Exception:
                    pass
        except Exception:
            self.printf.error("Holehe lookup failed")

    def search(self):
        self.printf.test("Running breach/leak checks for \"%s\"...\n" % self.email)
        self.check_emailrep()
        self.check_dehashed_light()
        self.check_holehe()

    def getbreaches(self):
        return self.breaches

    def process(self):
        self.search()
