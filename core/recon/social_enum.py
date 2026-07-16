#!/usr/bin/python3
# -*- coding: utf-8 -*-

import hashlib
import json
from core.lib import http
from core.lib import printer

class social_enum:
    printf = printer.printer()

    def __init__(self, email):
        self.email = email.lower().strip()
        self.results = {}

    def check_gravatar(self):
        self.printf.test("Checking Gravatar...")
        try:
            md5 = hashlib.md5(self.email.encode()).hexdigest()
            url = "https://www.gravatar.com/%s.json" % md5
            con = http.http()
            resp = con.get(url, timeout=10)
            if resp and '"entry"' in resp:
                data = json.loads(resp)
                entry = data.get('entry', [{}])[0]
                display = entry.get('displayName', 'Unknown')
                urls = entry.get('urls', [])
                photos = entry.get('photos', [])
                self.printf.plus("Gravatar: %s" % display)
                if photos:
                    self.printf.plus("  Photo: %s" % photos[0].get('value', ''))
                for u in urls:
                    self.printf.plus("  URL: %s" % u.get('value', ''))
                self.results['gravatar'] = {'name': display, 'urls': [u.get('value') for u in urls]}
            else:
                self.printf.error("No Gravatar found")
        except Exception:
            self.printf.error("Gravatar lookup failed")

    def check_github(self):
        self.printf.test("Checking GitHub...")
        try:
            con = http.http()
            url = "https://api.github.com/search/users?q=%s+in:email" % self.email
            resp = con.get(url, timeout=10)
            if resp:
                data = json.loads(resp)
                items = data.get('items', [])
                if items:
                    user = items[0]
                    self.printf.plus("GitHub: %s" % user.get('login', ''))
                    self.printf.plus("  Profile: %s" % user.get('html_url', ''))
                    self.printf.plus("  ID: %s" % user.get('id', ''))
                    self.results['github'] = {'login': user.get('login'), 'url': user.get('html_url')}
                else:
                    self.printf.error("No GitHub account found")
            else:
                self.printf.error("GitHub API failed")
        except Exception:
            self.printf.error("GitHub lookup failed")

    def check_keybase(self):
        self.printf.test("Checking Keybase...")
        try:
            con = http.http()
            url = "https://keybase.io/_/api/1.0/user/lookup.json?email=%s" % self.email
            resp = con.get(url, timeout=10)
            if resp:
                data = json.loads(resp)
                them = data.get('them', [])
                if them:
                    user = them[0]
                    basics = user.get('basics', {})
                    self.printf.plus("Keybase: %s" % basics.get('username', ''))
                    self.printf.plus("  Profile: https://keybase.io/%s" % basics.get('username', ''))
                    self.results['keybase'] = {'username': basics.get('username')}
                else:
                    self.printf.error("No Keybase account found")
        except Exception:
            self.printf.error("Keybase lookup failed")

    def check_twitter(self):
        self.printf.test("Checking Twitter/X (via nitter)...")
        try:
            con = http.http()
            username = self.email.split('@')[0]
            url = "https://nitter.net/%s" % username
            resp = con.get(url, timeout=10)
            if resp and 'Timeline' in resp and 'doesn\'t exist' not in resp:
                self.printf.plus("Twitter: @%s (likely)" % username)
                self.printf.plus("  Profile: https://x.com/%s" % username)
                self.results['twitter'] = {'username': username}
            else:
                self.printf.error("No Twitter account found for %s" % username)
        except Exception:
            self.printf.error("Twitter lookup failed")

    def check_linkedin(self):
        self.printf.test("Checking LinkedIn (via Google dork)...")
        try:
            con = http.http()
            url = "https://www.bing.com/search?q=site:linkedin.com+%22%s%22" % self.email.replace('@', '%40')
            resp = con.get(url, timeout=10)
            if resp and 'linkedin.com/in/' in resp:
                import re
                profiles = re.findall(r'linkedin\.com/in/([a-zA-Z0-9_-]+)', resp)
                if profiles:
                    self.printf.plus("LinkedIn: %s" % profiles[0])
                    self.printf.plus("  Profile: https://linkedin.com/in/%s" % profiles[0])
                    self.results['linkedin'] = {'profile': profiles[0]}
                else:
                    self.printf.error("No LinkedIn profile found")
            else:
                self.printf.error("No LinkedIn profile found")
        except Exception:
            self.printf.error("LinkedIn lookup failed")

    def check_avatar(self):
        self.printf.test("Checking Gravatar avatar...")
        try:
            md5 = hashlib.md5(self.email.encode()).hexdigest()
            avatar_url = "https://www.gravatar.com/avatar/%s?s=200&d=404" % md5
            con = http.http()
            resp = con.session.get(avatar_url, timeout=10)
            if resp.status_code == 200:
                self.printf.plus("Has Gravatar avatar: %s" % avatar_url)
                self.results['avatar'] = avatar_url
            else:
                self.printf.error("No Gravatar avatar")
        except Exception:
            pass

    def search(self):
        self.printf.test("Running social media enumeration for \"%s\"...\n" % self.email)
        self.check_gravatar()
        self.check_avatar()
        self.check_github()
        self.check_keybase()
        self.check_linkedin()

    def getresults(self):
        return self.results

    def process(self):
        self.search()
