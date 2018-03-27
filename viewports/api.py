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

	sales_orders = frappe.get_all('Sales Order')

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

@frappe.whitelist()
def get_arrivals(allow_guest=True):


	#Get harvests
	harvs = frappe.get_all('Harvest Request')
	harvests = {}
	for harv in harvs:
		harv_doc = frappe.get_doc('Harvest Request',harv['name'])
		harv = harv_doc.__dict__
		fish = harv["name"]
		#pp.pprint(harv)
		if harvests.get(fish) is not None:
			harvests[fish]["expected"] += int(harv["weight"])
		else:
			harvests[fish] = {
				"expected": int(harv["weight"]),
				"received": 0,
				"fish": harv["fish"],
				"time": harv["harvest_time"]
			}

	harvs = frappe.get_all('Harvest')
	print harvs
	for harv in harvs:
		harv_doc = frappe.get_doc('Harvest',harv['name'])
		harv = harv_doc.__dict__
		fish = harv["harvest_request"]
		if harvests.get(fish) is not None:
			harvests[fish]["received"] += int(harv["sample_weight"])

	harv_list = []
	for key in harvests:
		harv = harvests[key]
		percent_complete = float(harv["received"]) / float(harv["expected"])
		print percent_complete
		if percent_complete > 1:
			percent_complete = 1
		percent_complete = percent_complete*100
		percent_complete = str(percent_complete)
		harvests[key]["percent_complete"] = percent_complete
		harv_list.append(harvests[key])

	pp.pprint(harvests)

	#Get transfers
	transfers = frappe.get_all('Fish Transfer Request')
	tran_obj = {}
	for tran in transfers:
		tran_doc = frappe.get_doc('Fish Transfer Request',tran['name'])
		tran = tran_doc.__dict__
		pp.pprint(tran)

		farm_list = tran["farm"].split()
		farm = ""
		for word in farm_list:
			farm += word[0]
		tran_obj[tran["name"]] = {
			"expected": int(tran["weight"]),
			"received": 0,
			"farm": farm,
			"fish_variety": tran["fish_variety"]
		}

	transfers = frappe.get_all('Fish Transfer')
	for tran in transfers:
		tran_doc = frappe.get_doc('Fish Transfer',tran['name'])
		tran = tran_doc.__dict__
		#print tran['request']
		tran_obj[tran['request']]["received"] += int(tran['weight'])
		tran_obj[tran['request']]["time"] = tran["time"]
	

	tran_list = [tran_obj[key] for key in tran_obj if tran_obj[key]["received"] > 0]

	for idx,item in enumerate(tran_list):
		tran_list[idx]["percent_complete"] = int((float(item["received"]) / float(item["expected"])) * 100)

	pp.pprint(tran_list)



	return {"harvests":harv_list,"transfers":tran_list}
	
