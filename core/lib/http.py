#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# DarkSpy - Dragon Ball Z Hacker OSINT Suite
#
# @author:  darkLabz001
# @github:  https://github.com/darkLabz001/darkspy
# @license: MIT
#

import http.client
import ssl
import random
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

USER_AGENTS = [
    "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
]

class http:
    _tor_enabled = False

    def __init__(self, use_tor=False):
        self.session = requests.Session()
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        self.session.mount("https://", HTTPAdapter(max_retries=retries))
        self.session.mount("http://", HTTPAdapter(max_retries=retries))
        self.session.headers.update({
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        })
        if use_tor:
            self.enable_tor()

    def enable_tor(self, socks_port=9050):
        try:
            import socks
            socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", socks_port)
            socks.wrapmodule(requests)
            http._tor_enabled = True
        except ImportError:
            try:
                self.session.proxies = {
                    'http': 'socks5h://127.0.0.1:%d' % socks_port,
                    'https': 'socks5h://127.0.0.1:%d' % socks_port,
                }
                http._tor_enabled = True
            except Exception:
                pass

    @staticmethod
    def set_tor_global():
        http._tor_enabled = True

    def get(self, url, **kwargs):
        try:
            resp = self.session.get(url, timeout=15, **kwargs)
            return resp.text
        except Exception:
            return ""

    def httplib(self, server, query, cookie=None):
        try:
            ctx = ssl.create_default_context()
            con = http.client.HTTPSConnection(server, context=ctx, timeout=15)
            headers = {
                "Host": server,
                "User-Agent": random.choice(USER_AGENTS),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            }
            if cookie:
                headers["Cookie"] = cookie
            con.request('GET', query, headers=headers)
            response = con.getresponse()
            data = response.read()
            if isinstance(data, bytes):
                data = data.decode('utf-8', errors='ignore')
            return data
        except Exception:
            return ""

    def request(self, url):
        return self.get(url)

    def urllib(self, url, payload, headers=None):
        return self.get(url)
