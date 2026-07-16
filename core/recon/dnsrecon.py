#!/usr/bin/python3
# -*- coding: utf-8 -*-

import dns.resolver
from core.lib import printer

class dnsrecon:
    printf = printer.printer()

    def __init__(self, target):
        self.target = target
        self.emails = []
        self.mx_hosts = []

    def search(self):
        self.printf.test("Enumerating DNS/MX records for \"%s\"..." % self.target)

        try:
            mx_records = dns.resolver.resolve(self.target, 'MX')
            for mx in mx_records:
                host = str(mx.exchange).rstrip('.')
                self.mx_hosts.append(host)
                self.printf.plus("MX: %s (priority %s)" % (host, mx.preference))
        except Exception:
            self.printf.error("No MX records found")

        try:
            spf_records = dns.resolver.resolve(self.target, 'TXT')
            for txt in spf_records:
                record = str(txt).strip('"')
                if 'v=spf1' in record:
                    self.printf.plus("SPF: %s" % record)
                    import re
                    includes = re.findall(r'include:([^\s]+)', record)
                    for inc in includes:
                        self.printf.plus("  includes: %s" % inc)
        except Exception:
            pass

        try:
            ns_records = dns.resolver.resolve(self.target, 'NS')
            for ns in ns_records:
                self.printf.plus("NS: %s" % str(ns).rstrip('.'))
        except Exception:
            pass

        try:
            soa_records = dns.resolver.resolve(self.target, 'SOA')
            for soa in soa_records:
                rname = str(soa.rname).rstrip('.')
                if '@' in rname:
                    self.emails.append(rname)
                    self.printf.plus("SOA contact: %s" % rname)
        except Exception:
            pass

        for mx_host in self.mx_hosts:
            try:
                a_records = dns.resolver.resolve(mx_host, 'A')
                for a in a_records:
                    self.printf.plus("MX IP: %s -> %s" % (mx_host, str(a)))
            except Exception:
                pass

        if not self.emails:
            self.printf.error("No emails found via DNS")

    def getemail(self):
        return self.emails

    def process(self):
        self.search()
