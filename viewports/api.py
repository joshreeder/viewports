
import datetime

import frappe
import frappe.defaults

try:
	from .handlers.Arrivals import Arrivals
	from .handlers.SubAssembly import SubAssembly
	from .handlers.Trimming import Trimming
	from .handlers.Packing import Packing
	from .handlers.Packaging import Packaging
except Exception as ex:
	print(ex)

import pprint
pp = pprint.PrettyPrinter(indent=4)

@frappe.whitelist()
def get_packaging(allow_guest=True):
	try:
		data = Packaging().get_data()
	except Exception as ex:
		print(ex)
	return data


@frappe.whitelist()
def get_trimming(allow_guest=True):
	try:
		data = Trimming().get_data()
	except Exception as ex:
		print(ex)
	return data

@frappe.whitelist()
def get_packing(allow_guest=True):
	try:
		data = Packing().get_data()
	except Exception as ex:
		print(ex)
	return data

@frappe.whitelist()
def get_sub_assembly(allow_guest=True):
	try:
		data = SubAssembly().get_data()
	except Exception as ex:
		print(ex)
	return data

@frappe.whitelist()
def get_arrivals(allow_guest=True):

	data = Arrivals().get_data()
	return data


	