from __future__ import unicode_literals
import datetime

import frappe
import frappe.defaults

import pprint
pp = pprint.PrettyPrinter(indent=4)

@frappe.whitelist()
def get_header(allow_guest=True):
	harvs = frappe.get_all('Harvest')

	sales_orders = frappe.get_all('Sales Order')

	groups = {}
	for so in sales_orders:
		so_doc = frappe.get_doc('Sales Order',so['name'])
		for item in so_doc.items:
			item = item.__dict__
			#pp.pprint(item.__dict__)
			group = item["item_group"]
			if groups.get(group) is not None:
				groups[group] += item["total_weight"]
			else:
				groups[group] = item["total_weight"]
	#pp.pprint(groups)

	lbs_needed = sum([groups[key] for key in groups]) * 2

	lbs_needed = int(lbs_needed)

	#print "LBS needed",lbs_needed

	#print "SO",sales_orders

	#print "Harvs",harvs

	lbs_harvested = 0
	for harv in harvs:
		harv_doc = frappe.get_doc('Harvest',harv['name'])
		harv = harv_doc.__dict__
		lbs_harvested += int(harv['request_weight'])

	#print "LBS HAR",lbs_harvested

	percent_complete = ( float(lbs_harvested)/float(lbs_needed) ) * 100
	percent_complete = str(int(percent_complete)) + "%"

	#print "GetHeader",harv
	now = datetime.datetime.now()
	header = {
		"daily_average": "24,000",
		"weekday":now.strftime("%A"),
		"date":now.strftime("%b. %d"),
		"time": now.strftime("%H:%M"),
		"pounds_today": {
			"packed": lbs_harvested,
			"total":lbs_needed
		},
		"percent_complete":percent_complete,
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
	
