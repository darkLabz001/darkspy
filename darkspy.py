#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# DarkSpy - Hacker OSINT Intelligence Suite
# Email & Domain Intelligence Gathering Tool
#
# @author:  darkLabz001
# @github:  https://github.com/darkLabz001/darkspy
# @license: MIT
#

import json
import os
import sys
import getopt
import socket
import re
import requests
from urllib.parse import urlsplit
from core.lib import http
from core.lib import parser
from core.lib import color
from core.lib import printer
from core.lib import exporter
from core.recon import bing
from core.recon import pgp
from core.recon import netcraft
from core.recon import crtsh
from core.recon import dnsrecon
from core.recon import github_search
from core.recon import smtp_verify
from core.recon import hunter
from core.recon import social_enum
from core.recon import breach_check
from core.recon import header_analyze
from core.recon import subdomain_enum
from requests.packages.urllib3.exceptions import InsecureRequestWarning

SHODAN_KEY = "cvVdlWpSkYZL0YMT0lU1B0wV1SdmeYNJ"

class DarkSpy(object):
    color = color.Colors()
    printf = printer.printer()
    allemail = []
    use_tor = False
    export_json = False
    export_csv = False

    def banner(self):
        c = self.color
        print("")
        print(c.red(1)+"  ███████╗██╗   ██╗██████╗  ██████╗ ██████╗ ███████╗"+c.reset())
        print(c.red(1)+"  ██╔════╝██║   ██║██╔══██╗██╔═══██╗██╔══██╗██╔════╝"+c.reset())
        print(c.red(1)+"  █████╗  ██║   ██║██║  ██║██║   ██║██████╔╝███████╗"+c.reset())
        print(c.red(1)+"  ██╔══╝  ██║   ██║██║  ██║██║   ██║██╔══██╗╚════██║"+c.reset())
        print(c.red(1)+"  ██║     ╚██████╔╝██████╔╝╚██████╔╝██║  ██║███████║"+c.reset())
        print(c.red(1)+"  ╚═╝      ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝"+c.reset())
        print(c.white(0)+"                                                          "+c.reset())
        print(c.red(1)+"            ▀█▀ █▀▀ ▀▄▀ █▀▀ █▀ █ █ █▀▀ █▀▀█ █▀▄▀█"+c.reset())
        print(c.red(1)+"             █  ██▄  █  ██▄ ▄█ █▀█ ██▄ █▄▄▀ █ ▀ █"+c.reset())
        print(c.white(0)+"                                                          "+c.reset())
        print(c.red(1)+"       ╔═════════════════════════════════════════════╗"+c.reset())
        print(c.red(1)+"       ║        [-] HACKER OSINT INTELLIGENCE [-]   ║"+c.reset())
        print(c.red(1)+"       ║  Author:   darkLabz001                     ║"+c.reset())
        print(c.red(1)+"       ║  GitHub:   github.com/darkLabz001/darkspy  ║"+c.reset())
        print(c.red(1)+"       ║  Version:  1.0.0                           ║"+c.reset())
        print(c.red(1)+"       ║  License:  MIT                             ║"+c.reset())
        print(c.red(1)+"       ╚═════════════════════════════════════════════╝"+c.reset())
        print(c.white(0)+"                                                          "+c.reset())

    def tui_menu(self):
        c = self.color
        self.banner()
        print(c.red(1)+"  ╔══════════════════════════════════════════════════╗"+c.reset())
        print(c.red(1)+"  ║                  SELECT MODE                     ║"+c.reset())
        print(c.red(1)+"  ╠══════════════════════════════════════════════════╣"+c.reset())
        print(c.red(1)+"  ║                                                  ║"+c.reset())
        print(c.red(1)+"  ║  "+c.reset()+c.white(0)+"[1] Domain Reconnaissance                      "+c.red(1)+"║"+c.reset())
        print(c.red(1)+"  ║  "+c.reset()+c.white(0)+"[2] Email Info (Shodan Lookup)                 "+c.red(1)+"║"+c.reset())
        print(c.red(1)+"  ║  "+c.reset()+c.white(0)+"[3] Email SMTP Verify                         "+c.red(1)+"║"+c.reset())
        print(c.red(1)+"  ║  "+c.reset()+c.white(0)+"[4] Social Media Enumeration                  "+c.red(1)+"║"+c.reset())
        print(c.red(1)+"  ║  "+c.reset()+c.white(0)+"[5] Breach / Leak Check                       "+c.red(1)+"║"+c.reset())
        print(c.red(1)+"  ║  "+c.reset()+c.white(0)+"[6] Email Header Analysis (.eml)              "+c.red(1)+"║"+c.reset())
        print(c.red(1)+"  ║  "+c.reset()+c.white(0)+"[7] Subdomain Enumeration                     "+c.red(1)+"║"+c.reset())
        print(c.red(1)+"  ║  "+c.reset()+c.white(0)+"[8] Full Scan (All Sources)                   "+c.red(1)+"║"+c.reset())
        print(c.red(1)+"  ║  "+c.reset()+c.white(0)+"[0] Exit                                      "+c.red(1)+"║"+c.reset())
        print(c.red(1)+"  ║                                                  ║"+c.reset())
        print(c.red(1)+"  ╚══════════════════════════════════════════════════╝"+c.reset())
        print("")
        choice = input(c.red(1)+"  [?] Select option: "+c.reset())
        return choice.strip()

    def tui_domain_recon(self):
        c = self.color
        self.banner()
        print(c.red(1)+"  ╔══════════════════════════════════════════════════╗"+c.reset())
        print(c.red(1)+"  ║             DOMAIN RECONNAISSANCE                ║"+c.reset())
        print(c.red(1)+"  ╚══════════════════════════════════════════════════╝"+c.reset())
        print("")
        print(c.white(0)+"  Select source:"+c.reset())
        print(c.white(0)+"    [1] Bing Search"+c.reset())
        print(c.white(0)+"    [2] DNS / MX / SPF Records"+c.reset())
        print(c.white(0)+"    [3] PGP Keys"+c.reset())
        print(c.white(0)+"    [4] Certificate Transparency (crt.sh)"+c.reset())
        print(c.white(0)+"    [5] GitHub Code Search"+c.reset())
        print(c.white(0)+"    [6] Hunter.io"+c.reset())
        print(c.white(0)+"    [7] Subdomain Enumeration"+c.reset())
        print(c.white(0)+"    [8] ALL Sources"+c.reset())
        print("")
        source_choice = input(c.red(1)+"  [?] Select source: "+c.reset())
        target = input(c.red(1)+"  [?] Enter domain: "+c.reset()).strip()
        if not target:
            self.printf.error("No domain entered")
            return
        target = self.checkurl(target)
        self.banner()

        source_map = {
            '1': 'bing', '2': 'dns', '3': 'pgp', '4': 'crtsh',
            '5': 'github', '6': 'hunter', '7': 'subs', '8': 'all'
        }
        source = source_map.get(source_choice, 'all')

        sources = {
            'bing': lambda: self.bing(target),
            'pgp': lambda: self.pgp(target),
            'crtsh': lambda: self.crtsh(target),
            'dns': lambda: self.dns(target),
            'github': lambda: self.github(target),
            'hunter': lambda: self.hunter(target),
            'subs': lambda: self.subdomains(target),
        }

        if source == 'all':
            self.printf.test("Running all sources for \"%s\"...\n" % target)
            netcraft.netcraft(target).search()
            for name, func in sources.items():
                func()
        else:
            netcraft.netcraft(target).search()
            sources[source]()

        self.info()

    def tui_email_info(self):
        c = self.color
        self.banner()
        print(c.red(1)+"  ╔══════════════════════════════════════════════════╗"+c.reset())
        print(c.red(1)+"  ║           EMAIL INFO (SHODAN LOOKUP)             ║"+c.reset())
        print(c.red(1)+"  ╚══════════════════════════════════════════════════╝"+c.reset())
        print("")
        email = input(c.red(1)+"  [?] Enter email: "+c.reset()).strip()
        if '@' not in email:
            self.printf.error("Invalid email")
            return
        self.banner()
        self.getinfo(email)

    def tui_smtp_verify(self):
        c = self.color
        self.banner()
        print(c.red(1)+"  ╔══════════════════════════════════════════════════╗"+c.reset())
        print(c.red(1)+"  ║              EMAIL SMTP VERIFY                   ║"+c.reset())
        print(c.red(1)+"  ╚══════════════════════════════════════════════════╝"+c.reset())
        print("")
        email = input(c.red(1)+"  [?] Enter email: "+c.reset()).strip()
        if '@' not in email:
            self.printf.error("Invalid email")
            return
        self.banner()
        verify = smtp_verify.smtp_verify(email)
        verify.verify()

    def tui_social_enum(self):
        c = self.color
        self.banner()
        print(c.red(1)+"  ╔══════════════════════════════════════════════════╗"+c.reset())
        print(c.red(1)+"  ║         SOCIAL MEDIA ENUMERATION                ║"+c.reset())
        print(c.red(1)+"  ╚══════════════════════════════════════════════════╝"+c.reset())
        print("")
        email = input(c.red(1)+"  [?] Enter email: "+c.reset()).strip()
        if '@' not in email:
            self.printf.error("Invalid email")
            return
        self.banner()
        se = social_enum.social_enum(email)
        se.process()

    def tui_breach_check(self):
        c = self.color
        self.banner()
        print(c.red(1)+"  ╔══════════════════════════════════════════════════╗"+c.reset())
        print(c.red(1)+"  ║            BREACH / LEAK CHECK                   ║"+c.reset())
        print(c.red(1)+"  ╚══════════════════════════════════════════════════╝"+c.reset())
        print("")
        email = input(c.red(1)+"  [?] Enter email: "+c.reset()).strip()
        if '@' not in email:
            self.printf.error("Invalid email")
            return
        self.banner()
        bc = breach_check.breach_check(email)
        bc.process()

    def tui_header_analysis(self):
        c = self.color
        self.banner()
        print(c.red(1)+"  ╔══════════════════════════════════════════════════╗"+c.reset())
        print(c.red(1)+"  ║           EMAIL HEADER ANALYSIS                  ║"+c.reset())
        print(c.red(1)+"  ╚══════════════════════════════════════════════════╝"+c.reset())
        print("")
        path = input(c.red(1)+"  [?] Path to .eml file: "+c.reset()).strip()
        if not os.path.exists(path):
            self.printf.error("File not found: %s" % path)
            return
        self.banner()
        ha = header_analyze.header_analyze(path)
        ha.analyze()

    def tui_subdomain_enum(self):
        c = self.color
        self.banner()
        print(c.red(1)+"  ╔══════════════════════════════════════════════════╗"+c.reset())
        print(c.red(1)+"  ║           SUBDOMAIN ENUMERATION                 ║"+c.reset())
        print(c.red(1)+"  ╚══════════════════════════════════════════════════╝"+c.reset())
        print("")
        target = input(c.red(1)+"  [?] Enter domain: "+c.reset()).strip()
        if not target:
            self.printf.error("No domain entered")
            return
        target = self.checkurl(target)
        self.banner()
        se = subdomain_enum.subdomain_enum(target)
        se.process()

    def tui_full_scan(self):
        c = self.color
        self.banner()
        print(c.red(1)+"  ╔══════════════════════════════════════════════════╗"+c.reset())
        print(c.red(1)+"  ║              FULL SCAN (ALL SOURCES)             ║"+c.reset())
        print(c.red(1)+"  ╚══════════════════════════════════════════════════╝"+c.reset())
        print("")
        target = input(c.red(1)+"  [?] Enter domain: "+c.reset()).strip()
        if not target:
            self.printf.error("No domain entered")
            return
        target = self.checkurl(target)
        self.banner()
        self.printf.test("Running all sources for \"%s\"...\n" % target)
        netcraft.netcraft(target).search()
        self.bing(target)
        self.pgp(target)
        self.crtsh(target)
        self.dns(target)
        self.github(target)
        self.hunter(target)
        self.info()

    def run_tui(self):
        while True:
            choice = self.tui_menu()
            if choice == '1':
                self.tui_domain_recon()
            elif choice == '2':
                self.tui_email_info()
            elif choice == '3':
                self.tui_smtp_verify()
            elif choice == '4':
                self.tui_social_enum()
            elif choice == '5':
                self.tui_breach_check()
            elif choice == '6':
                self.tui_header_analysis()
            elif choice == '7':
                self.tui_subdomain_enum()
            elif choice == '8':
                self.tui_full_scan()
            elif choice == '0':
                print(self.color.red(1)+"\n  [!] Powering down DarkSpy..."+self.color.reset()+"\n")
                sys.exit(0)
            else:
                self.printf.error("Invalid option")
            print("")
            input(self.color.red(1)+"  [Press Enter to continue...]"+self.color.reset())

    def usage(self):
        name = os.path.basename(sys.argv[0]).split(".")[0]
        self.banner()
        print(self.color.red(1)+"  Usage: %s [options]\n" % (name) + self.color.reset())
        print(self.color.white(0)+"  Domain Recon:"+self.color.reset())
        print("\t-t --target\tDomain to search")
        print("\t-s --source\tData source: [all,bing,pgp,crtsh,dns,github,hunter,subs]")
        print("\t-d --subdomains\tEnumerate subdomains for a domain")
        print(self.color.white(0)+"  Email Recon:"+self.color.reset())
        print("\t-i --info\tGet email server info (Shodan)")
        print("\t-v --verify\tVerify email exists via SMTP")
        print("\t-p --social\tSocial media enumeration for an email")
        print("\t-b --breach\tCheck email for breaches/leaks")
        print("\t-H --header\tAnalyze email header (.eml file)")
        print(self.color.white(0)+"  Output:"+self.color.reset())
        print("\t-o --json\tExport results to JSON file")
        print("\t-c --csv\tExport results to CSV file")
        print("\t-O --output\tOutput directory")
        print(self.color.white(0)+"  Network:"+self.color.reset())
        print("\t-T --tor\tRoute requests through Tor")
        print("\t-h --help\tShow this help and exit")
        print(self.color.white(0)+"  TUI:"+self.color.reset())
        print("\t  --tui\t\tLaunch interactive menu (no args)")
        print("")
        print(self.color.red(1)+"  Examples:"+self.color.reset())
        print("\t %s --tui" % (name))
        print("\t %s -t site.com -s all" % (name))
        print("\t %s -i user@site.com" % (name))
        print("")

    def info(self):
        if self.allemail == []:
            self.printf.error("Not found email :(")
            return False
        allemail = []
        for x in self.allemail:
            if x not in allemail:
                allemail.append(x)
        print("")
        self.printf.plus("Found %d unique email(s)" % len(allemail))
        print("")
        try:
            for x in range(len(allemail)):
                self.printf.plus("Email: %s" % (allemail[x]))
                data = {'lang': 'en'}
                data['email'] = email[x]
                requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
                req = requests.post("http://mailtester.com/testmail.php", data=data, verify=False, timeout=10)
                regex = re.compile(r"[0-9]+(?:\.[0-9]+){3}")
                ip = regex.findall(req.content.decode('utf-8'))
                new = []
                for e in ip:
                    if e not in new:
                        new.append(e)
                for s in range(len(new)):
                    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
                    req = requests.get("https://api.shodan.io/shodan/host/" + new[s] + "?key=" + SHODAN_KEY, verify=False, timeout=10)
                    jso = json.loads(req.content.decode('utf-8'))
                    try:
                        self.sock = socket.gethostbyaddr(new[s])[0]
                    except socket.herror:
                        try:
                            self.sock = jso["hostnames"][0]
                        except KeyError:
                            self.sock = "unknown"
                    if "country_code" in jso and "country_name" in jso:
                        self.printf.ip("IP: %s (%s)" % (new[s], self.sock))
                        self.printf.info("Country: %s (%s)" % (jso["country_code"], jso["country_name"]))
                        self.printf.info("City: %s (%s)" % (jso["city"], jso["region_code"]))
                        self.printf.info("ASN: %s" % (jso["asn"]))
                        self.printf.info("ISP: %s" % (jso["isp"]))
                        self.printf.info("Geolocation: %s" % ("https://www.google.com/maps/@%s,%s,9z" % (jso["latitude"], jso["longitude"])))
                        self.printf.info("Hostname: %s" % (jso["hostnames"][0]))
                        self.printf.info("Organization: %s" % (jso["org"]))
                        self.printf.info("Ports: %s" % (jso["ports"]))
                        if "vulns" in jso:
                            self.printf.info("Vulns: %s" % (jso["vulns"][0]))
                        print("")
                    elif "No information available for that IP." in jso or "error" in jso:
                        self.printf.ip("IP: %s (%s)" % (new[s], self.sock))
                        self.printf.info("No information available for that ip :(", color="r")
                        print("")
                    else:
                        self.printf.ip("IP: %s (%s)" % (new[s], self.sock))
                        print("")
        except Exception:
            pass
        return True

    def checkurl(self, url):
        scheme = urlsplit(url).scheme
        netloc = urlsplit(url).netloc
        path = urlsplit(url).path
        if netloc == "":
            if path.startswith("www."):
                return path.split("www.")[1]
            else:
                return path
        if netloc != "":
            if netloc.startswith("www."):
                return netloc.split("www.")[1]
            else:
                return netloc

    def checkemail(self, email):
        if '@' not in email:
            self.banner()
            sys.exit(self.printf.error("Invalid email! Check your email"))
        return email

    def getinfo(self, email):
        self.printf.test("Checking email info...")
        domain = email.split('@')[1]
        try:
            import dns.resolver
            mx_records = dns.resolver.resolve(domain, 'MX')
            mx_host = str(sorted(mx_records, key=lambda r: r.preference)[0].exchange).rstrip('.')
            self.printf.plus("Email: %s" % email)
            self.printf.plus("MX Server: %s" % mx_host)
            ips = dns.resolver.resolve(mx_host, 'A')
            for a in ips:
                ip = str(a)
                self.printf.test("Looking up %s on Shodan..." % ip)
                try:
                    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
                    req = requests.get("https://api.shodan.io/shodan/host/%s?key=%s" % (ip, SHODAN_KEY), verify=False, timeout=10)
                    jso = json.loads(req.content.decode('utf-8'))
                    try:
                        self.sock = socket.gethostbyaddr(ip)[0]
                    except socket.herror:
                        try:
                            self.sock = jso["hostnames"][0]
                        except (KeyError, IndexError):
                            self.sock = "unknown"
                    if "country_code" in jso and "country_name" in jso:
                        self.printf.ip("IP: %s (%s)" % (ip, self.sock))
                        self.printf.info("Country: %s (%s)" % (jso["country_code"], jso["country_name"]))
                        self.printf.info("City: %s (%s)" % (jso.get("city", "?"), jso.get("region_code", "?")))
                        self.printf.info("ASN: %s" % (jso.get("asn", "?")))
                        self.printf.info("ISP: %s" % (jso.get("isp", "?")))
                        lat = jso.get("latitude", "0")
                        lon = jso.get("longitude", "0")
                        self.printf.info("Geolocation: %s" % ("https://www.google.com/maps/@%s,%s,9z" % (lat, lon)))
                        hosts = jso.get("hostnames", [])
                        if hosts:
                            self.printf.info("Hostname: %s" % (hosts[0]))
                        org = jso.get("org", "")
                        if org:
                            self.printf.info("Organization: %s" % org)
                        self.printf.info("Ports: %s" % (jso.get("ports", [])))
                        if "vulns" in jso:
                            self.printf.info("Vulns: %s" % (jso["vulns"][0]))
                    elif "error" in jso:
                        self.printf.ip("IP: %s (%s)" % (ip, self.sock))
                        self.printf.info("Shodan: %s" % jso["error"], color="r")
                    else:
                        self.printf.ip("IP: %s (%s)" % (ip, self.sock))
                    print("")
                except Exception as e:
                    self.printf.ip("IP: %s (%s)" % (ip, self.sock))
                    self.printf.info("Shodan lookup failed: %s" % str(e), color="r")
                    print("")
        except dns.resolver.NoAnswer:
            self.printf.error("No MX records found for %s" % domain)
        except dns.resolver.NXDOMAIN:
            self.printf.error("Domain %s does not exist" % domain)
        except Exception as e:
            self.printf.error("Error: %s" % str(e))

    def main(self, kwargs):
        if len(sys.argv) <= 1:
            self.run_tui()
            return

        if '--tui' in kwargs:
            self.run_tui()
            return

        try:
            opts, args = getopt.getopt(kwargs, "t:s:i:vh:H:dp:b:oO:cT",
                ["target=", "source=", "info=", "verify=", "help",
                 "header=", "subdomains", "social=", "breach=",
                 "json", "csv", "output=", "tor"])
        except Exception:
            self.usage()

        output_dir = None
        target = None

        for opt, arg in opts:
            if opt in ("-T", "--tor"):
                self.use_tor = True
                self.printf.test("Enabling Tor proxy...")
            if opt in ("-O", "--output"):
                output_dir = arg

        exp = None
        if target:
            exp = exporter.exporter(target, output_dir)

        for opt, arg in opts:
            if opt in ("-t", "--target"):
                target = self.checkurl(arg)
                exp = exporter.exporter(target, output_dir)
            if opt in ("-s", "--source"):
                source = arg
                valid = ("all", "bing", "pgp", "crtsh", "dns", "github", "hunter", "subs")
                if source not in valid:
                    self.banner()
                    sys.exit(self.printf.error("Invalid source! Try: %s" % ", ".join(valid)))
                self.banner()
                netcraft.netcraft(target).search()
                if source == "bing":
                    self.bing(target)
                    self.info()
                elif source == "pgp":
                    self.pgp(target)
                    self.info()
                elif source == "crtsh":
                    self.crtsh(target)
                    self.info()
                elif source == "dns":
                    self.dns(target)
                    self.info()
                elif source == "github":
                    self.github(target)
                    self.info()
                elif source == "hunter":
                    self.hunter(target)
                    self.info()
                elif source == "subs":
                    self.subdomains(target)
                    self.info()
                elif source == "all":
                    self.all(target)
                    self.info()
            if opt in ("-d", "--subdomains"):
                target = self.checkurl(arg) if arg else target
                if not target:
                    self.printf.error("Specify target with -t first")
                    sys.exit(1)
                self.banner()
                self.subdomains(target)
                self.info()
            if opt in ("-i", "--info"):
                email = self.checkemail(arg)
                self.banner()
                self.getinfo(email)
            if opt in ("-v", "--verify"):
                email = self.checkemail(arg)
                self.banner()
                self.verify_email(email)
            if opt in ("-p", "--social"):
                email = self.checkemail(arg)
                self.banner()
                self.social(email, exp)
            if opt in ("-b", "--breach"):
                email = self.checkemail(arg)
                self.banner()
                self.breach(email, exp)
            if opt in ("-H", "--header"):
                self.banner()
                self.header(arg)
            if opt in ("-o", "--json"):
                self.export_json = True
            if opt in ("-c", "--csv"):
                self.export_csv = True
            if opt in ("-h", "--help"):
                self.usage()

        if exp and (self.export_json or self.export_csv):
            exp.add_emails(self.allemail)
            if self.export_json:
                exp.export_json()
            if self.export_csv:
                exp.export_csv()

    def verify_email(self, email):
        verify = smtp_verify.smtp_verify(email)
        verify.verify()
        sys.exit()

    def social(self, email, exp=None):
        se = social_enum.social_enum(email)
        se.process()
        results = se.getresults()
        if exp:
            exp.add_social(results)
            if self.export_json:
                exp.export_json()
            if self.export_csv:
                exp.export_csv()

    def breach(self, email, exp=None):
        bc = breach_check.breach_check(email)
        bc.process()
        results = bc.getbreaches()
        if exp:
            exp.add_breaches(results)
            if self.export_json:
                exp.export_json()
            if self.export_csv:
                exp.export_csv()

    def header(self, path):
        ha = header_analyze.header_analyze(path)
        ha.analyze()
        results = ha.getresults()
        exp = exporter.exporter(results.get('from', 'unknown'))
        exp.add_header(results)
        if self.export_json:
            exp.export_json()
        if self.export_csv:
            exp.export_csv()

    def subdomains(self, domain, exp=None):
        se = subdomain_enum.subdomain_enum(domain)
        se.process()
        subs = se.getsubdomains()
        self.allemail.extend(se.getemails())
        if exp:
            exp.add_subdomains(subs)
            if self.export_json:
                exp.export_json()
            if self.export_csv:
                exp.export_csv()

    def bing(self, target):
        self.printf.test("Searching \"%s\" in Bing..." % target)
        search = bing.bing(target)
        search.process()
        emails = search.getemail()
        self.allemail.extend(emails)

    def pgp(self, target):
        self.printf.test("Searching \"%s\" in PGP..." % target)
        search = pgp.pgp(target)
        search.process()
        emails = search.getemail()
        self.allemail.extend(emails)

    def crtsh(self, target):
        search = crtsh.crtsh(target)
        search.process()
        emails = search.getemail()
        self.allemail.extend(emails)

    def dns(self, target):
        search = dnsrecon.dnsrecon(target)
        search.process()
        emails = search.getemail()
        self.allemail.extend(emails)

    def github(self, target):
        search = github_search.github(target)
        search.process()
        emails = search.getemail()
        self.allemail.extend(emails)

    def hunter(self, target):
        search = hunter.hunter_check(target)
        search.process()
        emails = search.getemail()
        self.allemail.extend(emails)

    def all(self, target):
        self.printf.test("Running all sources for \"%s\"...\n" % target)
        self.bing(target)
        self.pgp(target)
        self.crtsh(target)
        self.dns(target)
        self.github(target)
        self.hunter(target)


if __name__ == "__main__":
    try:
        DarkSpy().main(sys.argv[1:])
    except KeyboardInterrupt:
        print("\n" + "\033[1;31m" + "  [!] Interrupted. Powering down..." + "\033[0m")
        sys.exit(0)
