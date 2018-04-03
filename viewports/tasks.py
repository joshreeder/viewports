from __future__ import unicode_literals
import frappe
import datetime

def create_daily_summary():
	print "create_daily_summary called"
	print datetime.datetime.now()
	return