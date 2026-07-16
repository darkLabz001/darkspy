#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# DarkSpy - Dragon Ball Z Hacker OSINT Suite
#
# @author:  darkLabz001
# @github:  https://github.com/darkLabz001/darkspy
# @license: MIT
#


class Colors:

	def red(self,num):
		return "\033["+str(num)+";31m"

	def green(self,num):
		return "\033["+str(num)+";32m"

	def yellow(self,num):
		return "\033["+str(num)+";33m"

	def white(self,num):
		return "\033["+str(num)+";38m"

	def reset(self):
		return "\033[0m"

	def blue(self,num):
		return "\033["+str(num)+";34m"
