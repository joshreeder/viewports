from __future__ import unicode_literals
import datetime

import frappe
import frappe.defaults

@frappe.whitelist()
def get_header(allow_guest=True):
	now = datetime.datetime.now()
	header = {
		"daily_average": "24,000",
		"weekday":now.strftime("%A"),
		"date":now.strftime("%b. %d"),
		"time": now.strftime("%H:%M"),
		"pounds_today": {
			"packed": "18,482",
			"total":"27,500"
		},
		"percent_complete":"67%",
		"speed":"3,800"

	}
	return header

@frappe.whitelist()
def get_packaging(allow_guest=True):

	context = {}

	product = {
		"weight":"6-8",
		"name":"fre rrt fil",
		"completed":15,
		"total":20
	}

	products = [product for item in range(6)]

	page = {
		"products":products
	}

	context["page"] = page

	return context

@frappe.whitelist()
def get_trimming(allow_guest=True):
	context = {}
	trimmer = {"id":"e25","bins":14}

	context["trimmers"] = [trimmer for item in range(20)]

	context["pb"] = 34
	context["hopb"] = 22
	context["ho"] = 3
	context["pbf"] = 84
	context["cc"] = 21
	context["ccto"] = 13
	context["hbccto"] = 3

	context["trimmed"] = 180
	context["average"] = 193
	context["record"] = 212

	return context

@frappe.whitelist()
def get_packing(allow_guest=True):
	context = {}
	item = {}
	item["name"] = "4-6oz frs rrt fil"
	item["quantity"] = 4
	item["percent_complete"] = "50%"

	context["customers"] = []
	for idx in range(3):
		customer = {}
		customer["name"] = "sysco"
		customer["items_total"] = 24
		customer["items_completed"] = 4
		customer["items"] = [item for x in range(3)]
		context["customers"].append(customer)

	return context

@frappe.whitelist()
def get_sub_assembly(allow_guest=True):
	context = {}
	item = {}
	item["name"] = "red fillets"
	item["bins"] = {"completed":12,"total":18}

	context["items"] = [item for x in range(5)]

	return context
	
