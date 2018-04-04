from __future__ import unicode_literals
import frappe
import datetime

import pprint

try:
	from handlers.Arrivals import Arrivals
	from handlers.SubAssembly import SubAssembly
	from handlers.Trimming import Trimming
	from handlers.Packing import Packing
	from handlers.Packaging import Packaging
except Exception as ex:
	print(ex)

pp = pprint.PrettyPrinter(indent=4)

def create_daily_summary():

	temp_dict = {}

	arrivals = Arrivals().get_page()
	tdate = Arrivals().tdate

	# Transfers
	transfers = []
	requested = 0
	actual = 0
	for item in arrivals['transfers']:
		doc = frappe.new_doc("Daily Report Item")
		doc.update({"item_name":item["fish_variety"],"requested":item["expected"],"actual":item["received"]})
		transfers.append(doc)
		requested += item["expected"]
		actual += item["received"]

	doc = frappe.new_doc("Daily Report Item")
	doc.update({
		"item_name":"Transfers",
		"requested":requested,
		"actual":actual,
		"daily_report_items":transfers})

	transfers = doc

	temp_dict["transfer_requested"] = requested
	temp_dict["transfer_actual"] = actual

	# Harvests
	harvests = []
	requested = 0
	actual = 0
	for item in arrivals['harvests']:
		doc = frappe.new_doc("Daily Report Item")
		doc.update({"item_name":item["fish"],"requested":item["expected"],"actual":item["received"]})
		harvests.append(doc)
		requested += item["expected"]
		actual += item["received"]

	doc = frappe.new_doc("Daily Report Item")
	doc.update({
		"item_name":"Harvests",
		"requested":requested,
		"actual":actual,
		"daily_report_items":harvests})

	harvests = doc

	temp_dict["harvest_requested"] = requested
	temp_dict["harvest_actual"] = actual

	# # Transfers
	# # Still need to implement sub items
	# transfers = Arrivals().get_data()
	# requested = transfers['header']['pounds_today']['total']
	# actual = transfers['header']['pounds_today']['packed']
	# doc = frappe.new_doc("Daily Report Item")
	# doc.update({
	# 	"item_name":"Transfers",
	# 	"requested":requested,
	# 	"actual":actual})

	# transfers = doc

	# # Harvests
	# harvests = transfers


	# Trimming
	# Still need to implement sub items
	trimming = Trimming().get_data()
	requested = trimming['header']['pounds_today']['total']
	actual = trimming['header']['pounds_today']['packed']
	doc = frappe.new_doc("Daily Report Item")
	doc.update({
		"item_name":"Trimmed",
		"requested":requested,
		"actual":actual})

	trimmed = doc

	temp_dict["trimmed_requested"] = requested
	temp_dict["trimmed_actual"] = actual

	pp.pprint(trimmed.__dict__)

	# Packaging
	# Still need to implement sub items
	packing = Packing().get_data()
	requested = packing['header']['pounds_today']['total']
	actual = packing['header']['pounds_today']['packed']
	doc = frappe.new_doc("Daily Report Item")
	doc.update({
		"item_name":"Packaged",
		"requested":requested,
		"actual":actual})
	packaged = doc

	temp_dict["packaged_requested"] = requested
	temp_dict["packaged_actual"] = actual

	# Shipping
	# Still need to implement sub items
	packing = Packaging().get_data()
	requested = packing['header']['pounds_today']['total']
	actual = packing['header']['pounds_today']['packed']
	doc = frappe.new_doc("Daily Report Item")
	doc.update({
		"item_name":"Shipped",
		"requested":requested,
		"actual":actual})

	shipped = {
		"item_name":"Shipped",
		"requested":requested,
		"actual":actual
	}

	temp_dict["shipped_requested"] = requested
	temp_dict["shipped_actual"] = actual

	temp_dict["date"] = tdate

	## GET DOC

	# print "getting doc..."
	# dr_doc = frappe.get_doc({
	# 	"doctype":"Processing Plant Daily Report",
	# 	"harvests":[],
	# 	"transfers":[],
	# 	"trimmed": [],
	# 	"packaged": [],
	# 	"shipped": [],
	# 	"date":tdate
	# 	})
	# dr_doc.append("harvests", shipped)
	# print "inserting..."
	# dr_doc.insert()
	# print "submiting..."
	# print "Saving..."
	# dr_doc.save(ignore_permissions=True)
	# frappe.db.commit()

	##END GET DOC

	# ## NEW DOC
	# dr_doc = frappe.new_doc("Processing Plant Daily Report")

	# print "Updating..."
	# pp.pprint([shipped])
	# dr_doc.update({
	# 	"harvests":[harvests],
	# 	"transfers":[transfers],
	# 	"trimmed": [trimmed],
	# 	"packaged": [packaged],
	# 	"shipped": [shipped],
	# 	"date":tdate
	# 	})
	# pp.pprint(dr_doc.__dict__)
	# print "Saving..."
	# dr_doc.save(ignore_permissions=True)
	# frappe.db.commit()

	# print "Daily Report Saved"
	# ## END NEW DOC

	## TEMP NEW DOC
	dr_doc = frappe.new_doc("Processing Plant Daily Report Temp")

	print "Updating..."
	pp.pprint([shipped])
	dr_doc.update(temp_dict)
	pp.pprint(dr_doc.__dict__)
	print "Saving..."
	dr_doc.save(ignore_permissions=True)
	frappe.db.commit()

	print "Daily Report Saved"
	## END TEMP NEW DOC



	return