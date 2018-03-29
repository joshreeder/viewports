from __future__ import unicode_literals
import datetime

import frappe
import frappe.defaults

try:
	from handlers.Arrivals import Arrivals
	from handlers.SubAssembly import SubAssembly
except Exception as ex:
	print(ex)


import pprint
pp = pprint.PrettyPrinter(indent=4)

tdate = datetime.datetime.strptime('27032018', "%d%m%Y").date()


def get_docs(doctype):
	docs = frappe.get_all(doctype)
	doc_objs = []
	for doc in docs:
		doc = frappe.get_doc(doctype,doc['name'])
		doc_objs.append(doc)
	return doc_objs



@frappe.whitelist()
def get_header(allow_guest=True):

	
	sales_orders = frappe.get_all("Sales Order", fields=["*"])
	sales_orders = [item for item in sales_orders if item['delivery_date'] == tdate]

	harv_reqs = frappe.get_all("Harvest Request", fields=["*"])
	harv_reqs = [item for item in harv_reqs if item['harvest_date'] == tdate]

	groups = {}
	for so in sales_orders:
		so = frappe.get_doc('Sales Order',so['name'])
		so = so.__dict__
		items = so["items"]
		for item in items:
			item = item.__dict__
			#pp.pprint(item.__dict__)
			group = item["item_group"]
			if groups.get(group) is not None:
				groups[group] += item["total_weight"]
			else:
				groups[group] = item["total_weight"]

	lbs_needed = sum([groups[key] for key in groups]) * 2
	lbs_needed = int(lbs_needed)

	lbs_harvested = 0
	for harv in harv_reqs:
		lbs_harvested += int(harv['weight'])

	percent_complete = ( float(lbs_harvested)/float(lbs_needed) ) * 100
	percent_complete = str(int(percent_complete)) + "%"

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

	sales_orders = frappe.get_all('Sales Order', fields=["*"])
	sales_orders = [item for item in sales_orders if item['delivery_date'] == tdate]

	item_codes = {}
	for so in sales_orders:
		so_doc = frappe.get_doc('Sales Order',so['name'])
		for item in so_doc.items:
			item = item.__dict__
			item_code = item.get("item_code")
			if item_codes.get(item_code) is not None:
				item_codes[item_code] += item["qty"]
			else:
				item_codes[item_code] = item["qty"]
	pp.pprint(item_codes)

	products = []

	for key in item_codes:
		item = {
			"weight":"?",
			"name":key,
			"completed":"?",
			"total":item_codes[key]
		}
		products.append(item)


	# product = {
	# 	"weight":"6-8",
	# 	"name":"fre rrt fil",
	# 	"completed":15,
	# 	"total":20
	# }

	# products = [product for item in range(6)]

	page = {
		"products":products
	}

	context["page"] = page

	return context

@frappe.whitelist()
def get_trimming(allow_guest=True):
	context = {}
	trimmer = {"id":"e25","bins":14}

	trimmers = frappe.get_all("Trimmer Code")
	trimmer_objs = []
	for trim in trimmers:
		trim_doc = frappe.get_doc('Trimmer Code',trim['name'])
		trim = trim_doc.__dict__
		obj = {
			"name": trim["name"],
			"trimmer_number": trim["trimmer_number"]
		}
		trimmer_objs.append(obj)

	context["trimmers"] = trimmer_objs

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

	sales_orders = frappe.get_all('Sales Order', fields=["*"])
	sales_orders = [item for item in sales_orders if item['delivery_date'] == tdate]

	orders = []
	for so in sales_orders:
		so_doc = frappe.get_doc('Sales Order',so['name'])
		order = {
			"company":so_doc.customer_name,
			"items":[],
			"total_quantity": 0,
			"total_packed": 0
		}
		for item in so_doc.items:
			item = item.__dict__
			order_item = {
				"packed": 0,
				"quantity": int(item['qty']),
				"item_code": item['item_code']
			}
			order["total_quantity"] += int(item['qty'])
			order["items"].append(order_item)
		orders.append(order)

	pp.pprint(orders)

	return {"orders":orders}



	# context = {}
	# item = {}
	# item["name"] = "4-6oz frs rrt fil"
	# item["quantity"] = 4
	# item["percent_complete"] = "50%"

	# context["customers"] = []
	# for idx in range(3):
	# 	customer = {}
	# 	customer["name"] = "sysco"
	# 	customer["items_total"] = 24
	# 	customer["items_completed"] = 4
	# 	customer["items"] = [item for x in range(3)]
	# 	context["customers"].append(customer)

	# return context

@frappe.whitelist()
def get_sub_assembly(allow_guest=True):
	try:
		data = SubAssembly().get_data()
	except Exception as ex:
		print ex
	return data

@frappe.whitelist()
def get_arrivals(allow_guest=True):

	data = Arrivals().get_data()
	return data


	