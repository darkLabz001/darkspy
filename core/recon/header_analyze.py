#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import email
import sys
from datetime import datetime
from core.lib import printer

class header_analyze:
    printf = printer.printer()

    def __init__(self, eml_path):
        self.eml_path = eml_path
        self.headers = {}
        self.body = ""
        self.analysis = {}

    def parse(self):
        try:
            with open(self.eml_path, 'r', errors='ignore') as f:
                raw = f.read()
            msg = email.message_from_string(raw)
            for key in ('From', 'To', 'Cc', 'Bcc', 'Subject', 'Date',
                        'Message-ID', 'X-Mailer', 'Return-Path', 'Reply-To',
                        'Received', 'SPF', 'DKIM-Signature', 'Authentication-Results',
                        'X-Originating-IP', 'X-Sender-IP'):
                val = msg.get(key, None)
                if val:
                    self.headers[key] = val
            if msg.is_multipart():
                for part in msg.walk():
                    ct = part.get_content_type()
                    if ct == 'text/plain':
                        self.body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
            else:
                self.body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            return True
        except Exception as e:
            self.printf.error("Failed to parse email: %s" % str(e))
            return False

    def extract_ips(self):
        ips = set()
        received = self.headers.get('Received', '')
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        found = re.findall(ip_pattern, received)
        ips.update(found)
        originating = self.headers.get('X-Originating-IP', '')
        if originating:
            found = re.findall(ip_pattern, originating)
            ips.update(found)
        sender_ip = self.headers.get('X-Sender-IP', '')
        if sender_ip:
            found = re.findall(ip_pattern, sender_ip)
            ips.update(found)
        return list(ips)

    def extract_domains(self):
        domains = set()
        received = self.headers.get('Received', '')
        from_match = re.findall(r'from\s+(\S+)', received)
        domains.update(from_match)
        by_match = re.findall(r'by\s+(\S+)', received)
        domains.update(by_match)
        msg_id = self.headers.get('Message-ID', '')
        if msg_id:
            domain_match = re.findall(r'@([\w.-]+)', msg_id)
            domains.update(domain_match)
        return list(domains)

    def check_spf(self):
        auth = self.headers.get('Authentication-Results', '')
        spf_match = re.search(r'spf=(\w+)', auth)
        if spf_match:
            return spf_match.group(1)
        return 'not found'

    def check_dkim(self):
        auth = self.headers.get('Authentication-Results', '')
        dkim_match = re.search(r'dkim=(\w+)', auth)
        if dkim_match:
            return dkim_match.group(1)
        return 'not found'

    def check_dmarc(self):
        auth = self.headers.get('Authentication-Results', '')
        dmarc_match = re.search(r'dmarc=(\w+)', auth)
        if dmarc_match:
            return dmarc_match.group(1)
        return 'not found'

    def trace_route(self):
        received = self.headers.get('Received', '')
        hops = re.findall(r'from\s+(\S+)\s.*?by\s+(\S+)', received)
        return hops

    def analyze(self):
        self.printf.test("Analyzing email headers from \"%s\"...\n" % self.eml_path)
        if not self.parse():
            return

        self.printf.plus("Basic Information:")
        self.printf.info("From: %s" % self.headers.get('From', 'N/A'))
        self.printf.info("To: %s" % self.headers.get('To', 'N/A'))
        self.printf.info("Subject: %s" % self.headers.get('Subject', 'N/A'))
        self.printf.info("Date: %s" % self.headers.get('Date', 'N/A'))
        self.printf.info("Message-ID: %s" % self.headers.get('Message-ID', 'N/A'))
        self.printf.info("X-Mailer: %s" % self.headers.get('X-Mailer', 'N/A'))
        print("")

        self.printf.plus("Email Authentication:")
        self.printf.info("SPF: %s" % self.check_spf())
        self.printf.info("DKIM: %s" % self.check_dkim())
        self.printf.info("DMARC: %s" % self.check_dmarc())
        print("")

        ips = self.extract_ips()
        if ips:
            self.printf.plus("IP Addresses Found:")
            for ip in ips:
                self.printf.info("  %s" % ip)
            print("")

        domains = self.extract_domains()
        if domains:
            self.printf.plus("Domains Found:")
            for d in domains:
                self.printf.info("  %s" % d)
            print("")

        hops = self.trace_route()
        if hops:
            self.printf.plus("Route Trace (%d hops):" % len(hops))
            for i, (fr, by) in enumerate(hops, 1):
                self.printf.info("  %d. %s -> %s" % (i, fr, by))
            print("")

        self.analysis = {
            'from': self.headers.get('From', ''),
            'to': self.headers.get('To', ''),
            'subject': self.headers.get('Subject', ''),
            'date': self.headers.get('Date', ''),
            'message_id': self.headers.get('Message-ID', ''),
            'x_mailer': self.headers.get('X-Mailer', ''),
            'spf': self.check_spf(),
            'dkim': self.check_dkim(),
            'dmarc': self.check_dmarc(),
            'ips': ips,
            'domains': domains,
            'hops': len(hops),
            'return_path': self.headers.get('Return-Path', ''),
            'reply_to': self.headers.get('Reply-To', ''),
        }

    def getresults(self):
        return self.analysis
