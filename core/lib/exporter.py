#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# DarkSpy - Dragon Ball Z Hacker OSINT Suite
#
# @author:  darkLabz001
# @github:  https://github.com/darkLabz001/darkspy
# @license: MIT
#

import json
import csv
import os
from core.lib import printer

class exporter:
    printf = printer.printer()

    def __init__(self, target, output_dir=None):
        self.target = target
        self.data = {
            'target': target,
            'emails': [],
            'social': {},
            'breaches': [],
            'subdomains': [],
            'dns': {},
            'header_analysis': {},
        }
        if output_dir:
            self.output_dir = output_dir
        else:
            self.output_dir = os.path.expanduser("~/tools/Infoga/output")
        os.makedirs(self.output_dir, exist_ok=True)

    def add_emails(self, emails):
        self.data['emails'] = list(set(emails))

    def add_social(self, social):
        self.data['social'] = social

    def add_breaches(self, breaches):
        self.data['breaches'] = breaches

    def add_subdomains(self, subdomains):
        self.data['subdomains'] = subdomains

    def add_dns(self, dns_info):
        self.data['dns'] = dns_info

    def add_header(self, header_info):
        self.data['header_analysis'] = header_info

    def export_json(self, filename=None):
        if not filename:
            filename = "infoga_%s.json" % self.target.replace('.', '_')
        path = os.path.join(self.output_dir, filename)
        try:
            with open(path, 'w') as f:
                json.dump(self.data, f, indent=2, default=str)
            self.printf.plus("JSON exported: %s" % path)
            return path
        except Exception as e:
            self.printf.error("JSON export failed: %s" % str(e))
            return None

    def export_csv(self, filename=None):
        if not filename:
            filename = "infoga_%s.csv" % self.target.replace('.', '_')
        path = os.path.join(self.output_dir, filename)
        try:
            with open(path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Type', 'Key', 'Value'])
                for email in self.data['emails']:
                    writer.writerow(['email', '', email])
                for platform, info in self.data['social'].items():
                    if isinstance(info, dict):
                        for k, v in info.items():
                            writer.writerow(['social', platform, '%s: %s' % (k, v)])
                    else:
                        writer.writerow(['social', platform, str(info)])
                for breach in self.data['breaches']:
                    if isinstance(breach, dict):
                        writer.writerow(['breach', breach.get('name', breach.get('source', '')), json.dumps(breach)])
                for sub in self.data['subdomains']:
                    writer.writerow(['subdomain', '', sub])
            self.printf.plus("CSV exported: %s" % path)
            return path
        except Exception as e:
            self.printf.error("CSV export failed: %s" % str(e))
            return None

    def print_summary(self):
        print("")
        self.printf.plus("=" * 50)
        self.printf.plus("REPORT SUMMARY for %s" % self.target)
        self.printf.plus("=" * 50)
        self.printf.info("Emails found: %d" % len(self.data['emails']))
        for e in self.data['emails']:
            self.printf.info("  - %s" % e)
        if self.data['social']:
            self.printf.info("Social profiles found: %d" % len(self.data['social']))
            for platform, info in self.data['social'].items():
                if isinstance(info, dict):
                    self.printf.info("  - %s: %s" % (platform, info.get('login', info.get('username', info.get('name', str(info))))))
                else:
                    self.printf.info("  - %s: %s" % (platform, info))
        if self.data['breaches']:
            self.printf.info("Breach records: %d" % len(self.data['breaches']))
        if self.data['subdomains']:
            self.printf.info("Subdomains found: %d" % len(self.data['subdomains']))
        self.printf.plus("=" * 50)
        print("")
