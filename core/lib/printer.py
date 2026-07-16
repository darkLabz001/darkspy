#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# DarkSpy - Dragon Ball Z Hacker OSINT Suite
#
# @author:  darkLabz001
# @github:  https://github.com/darkLabz001/darkspy
# @license: MIT
#

from core.lib import color

class printer:
    #
    red = color.Colors().red(1)
    white = color.Colors().white(0)
    green = color.Colors().green(1)
    blue = color.Colors().blue(1)
    end = color.Colors().reset()
    #
    def plus(self, string, flag="+"):
        print("%s[%s]%s %s%s%s" % (self.green, flag, self.end, self.white, string, self.end))

    def test(self, string, flag="*"):
        print("%s[%s]%s %s%s%s" % (self.blue, flag, self.end, self.blue, string, self.end))

    def error(self, string, flag="!"):
        print("%s[%s]%s %s%s%s" % (self.red, flag, self.end, self.red, string, self.end))

    def ip(self, string, flag="|"):
        print(" %s%s%s  %s%s%s\n" % (self.green, flag, self.end, self.white, string, self.end))

    def info(self, string, color="g", flag="|"):
        if color == "g":
            print("\t  %s%s%s  %s%s%s" % (self.green, flag, self.end, self.white, string, self.end))
        if color == "r":
            print("\t  %s%s%s  %s%s%s" % (self.red, flag, self.end, self.red, string, self.end))
