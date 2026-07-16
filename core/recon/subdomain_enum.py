#!/usr/bin/python3
# -*- coding: utf-8 -*-

import dns.resolver
from core.lib import http
from core.lib import printer

class subdomain_enum:
    printf = printer.printer()

    def __init__(self, domain):
        self.domain = domain
        self.subdomains = []
        self.emails = []

    def crtsh_enum(self):
        self.printf.test("Enumerating subdomains via crt.sh...")
        try:
            import json
            con = http.http()
            url = "https://crt.sh/?q=.%s&output=json" % self.domain
            resp = con.get(url, timeout=20)
            if resp and '<html' not in resp[:200].lower():
                data = json.loads(resp)
                for entry in data:
                    name = entry.get('name_value', '')
                    for line in name.split('\n'):
                        line = line.strip().lower()
                        if line.endswith('.' + self.domain) or line == self.domain:
                            if line not in self.subdomains:
                                self.subdomains.append(line)
                self.printf.plus("Found %d subdomains from crt.sh" % len(self.subdomains))
            else:
                self.printf.error("crt.sh unavailable")
        except Exception:
            self.printf.error("crt.sh enumeration failed")

    def dns_brute(self):
        self.printf.test("Brute-forcing common subdomains...")
        prefixes = [
            'mail', 'smtp', 'pop', 'imap', 'webmail', 'mx', 'mx1', 'mx2',
            'ns1', 'ns2', 'ns3', 'dns', 'dns1', 'dns2',
            'www', 'ftp', 'sftp', 'vpn', 'remote', 'gateway',
            'admin', 'panel', 'cpanel', 'whm', 'webmin',
            'api', 'dev', 'staging', 'test', 'beta', 'alpha',
            'blog', 'forum', 'shop', 'store', 'portal',
            'git', 'gitlab', 'github', 'bitbucket', 'svn',
            'vpn', 'openvpn', 'wireguard', 'ipsec',
            'db', 'database', 'mysql', 'postgres', 'mongo', 'redis', 'elastic',
            'kibana', 'grafana', 'prometheus', 'monitor',
            'jenkins', 'ci', 'cd', 'deploy', 'build',
            'backup', 'bak', 'old', 'archive', 'legacy',
            'cdn', 'static', 'assets', 'media', 'img', 'images',
            'status', 'health', 'uptime', 'monitor',
            'autodiscover', 'autoconfig', 'relay',
            'owa', 'activesync', 'exchange', 'lync',
            'proxy', 'load', 'balancer', 'haproxy', 'nginx',
            'intranet', 'internal', 'corp', 'office',
            'files', 'share', 'sharepoint', 'onedrive',
            'hr', 'crm', 'erp', 'jira', 'confluence',
        ]
        found = 0
        for prefix in prefixes:
            sub = "%s.%s" % (prefix, self.domain)
            try:
                answers = dns.resolver.resolve(sub, 'A')
                for a in answers:
                    self.subdomains.append(sub)
                    self.printf.plus("Found: %s -> %s" % (sub, str(a)))
                    found += 1
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
                pass
            except Exception:
                pass
        if found == 0:
            self.printf.error("No subdomains found via brute-force")

    def find_emails(self):
        self.printf.test("Finding emails on discovered subdomains...")
        for sub in self.subdomains:
            try:
                mx_records = dns.resolver.resolve(sub, 'MX')
                for mx in mx_records:
                    host = str(mx.exchange).rstrip('.')
                    self.printf.plus("MX on %s: %s" % (sub, host))
            except Exception:
                pass
            try:
                txt_records = dns.resolver.resolve(sub, 'TXT')
                for txt in txt_records:
                    record = str(txt).strip('"')
                    if 'v=spf1' in record:
                        self.printf.plus("SPF on %s: %s" % (sub, record[:80]))
            except Exception:
                pass

    def search(self):
        self.printf.test("Running subdomain enumeration for \"%s\"...\n" % self.domain)
        self.crtsh_enum()
        self.dns_brute()
        self.find_emails()

    def getsubdomains(self):
        return self.subdomains

    def getemails(self):
        return self.emails

    def process(self):
        self.search()
