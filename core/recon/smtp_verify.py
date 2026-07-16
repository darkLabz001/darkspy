#!/usr/bin/python3
# -*- coding: utf-8 -*-

import smtplib
import dns.resolver
import socket
from core.lib import printer

class smtp_verify:
    printf = printer.printer()

    def __init__(self, email):
        self.email = email
        self.domain = email.split('@')[1]
        self.exists = False
        self.mx_host = None

    def get_mx(self):
        try:
            mx_records = dns.resolver.resolve(self.domain, 'MX')
            mx_hosts = [(str(r.exchange).rstrip('.'), r.preference) for r in mx_records]
            mx_hosts.sort(key=lambda x: x[1])
            return mx_hosts[0][0] if mx_hosts else None
        except Exception:
            return None

    def verify(self):
        self.mx_host = self.get_mx()
        if not self.mx_host:
            self.printf.error("No MX records found for %s" % self.domain)
            return False

        self.printf.test("Connecting to MX: %s" % self.mx_host)
        try:
            server = smtplib.SMTP(timeout=10)
            server.connect(self.mx_host, 25)
            server.helo("infoga.local")
            server.mail("test@infoga.local")
            code, msg = server.rcpt(self.email)
            server.quit()

            if code == 250:
                self.exists = True
                self.printf.plus("Email EXISTS (SMTP verification passed)")
                return True
            elif code == 550:
                self.printf.error("Email DOES NOT EXIST (rejected by server)")
                return False
            else:
                self.printf.test("Server returned code %d - cannot verify" % code)
                return False
        except smtplib.SMTPServerDisconnected:
            self.printf.error("Server disconnected (may be blocking verification)")
            return False
        except smtplib.SMTPConnectError:
            self.printf.error("Could not connect to MX server")
            return False
        except socket.timeout:
            self.printf.error("Connection timed out")
            return False
        except Exception as e:
            self.printf.error("SMTP error: %s" % str(e))
            return False
