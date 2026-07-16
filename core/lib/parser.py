#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# DarkSpy - Dragon Ball Z Hacker OSINT Suite
#
# @author:  darkLabz001
# @github:  https://github.com/darkLabz001/darkspy
# @license: MIT
#

import re

class parser:

    def __init__(self, results, target):
        self.results = results
        self.target = target

    def clean(self):
        for tag in ('<em>', '</em>', '<b>', '</b>', '<strong>', '</strong>',
                     '<wbr>', '</wbr>', '<span>', '</span>', '<div>', '</div>',
                     '<br>', '<br/>', '<br />', '<p>', '</p>', '<li>', '</li>',
                     '<td>', '</td>', '<tr>', '</tr>', '<a ', '</a>'):
            self.results = self.results.replace(tag, " ")
        self.results = re.sub(r'<[^>]+>', ' ', self.results)
        for x in ('>', ':', '=', '<', '/', '\\', ';', '&', '%2f', '%3a', '%3A', '%3D', '%3C', '%40'):
            self.results = self.results.replace(x, " ")

    def email(self):
        self.clean()
        patterns = [
            r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}',
            r'mailto:([a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})',
            r'["\']([a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})["\']',
        ]
        fake_emails = {
            'error-lite@duckduckgo.com', 'noreply@duckduckgo.com',
            'privacy@duckduckgo.com', 'test@example.com',
            'user@example.com', 'email@example.com',
            'example@example.com', 'admin@example.com',
            'info@example.com', 'contact@example.com',
            'support@example.com', 'null@localhost',
            'root@localhost', 'postmaster@localhost',
            'webmaster@localhost', 'name@example.com',
            'your@email.com', 'someone@example.com',
        }
        emails = []
        for pattern in patterns:
            for match in re.findall(pattern, self.results, re.IGNORECASE):
                email = match.lower().strip()
                if (email not in emails
                    and email not in fake_emails
                    and not email.startswith('abuse@')
                    and '%' not in email
                    and len(email) > 5
                    and '.' in email.split('@')[1]
                    and self.target.split('.')[0] not in email.split('@')[0]):
                    emails.append(email)
        return emails

    def email_from_text(self):
        self.clean()
        pattern = r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
        emails = []
        for match in re.findall(pattern, self.results, re.IGNORECASE):
            email = match.lower().strip()
            if (email not in emails
                and '%' not in email
                and len(email) > 5
                and '.' in email.split('@')[1]):
                emails.append(email)
        return emails
