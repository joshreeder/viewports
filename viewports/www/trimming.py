
import frappe
import datetime
import pprint
pp = pprint.PrettyPrinter(indent=4)
import viewports.api as api

def get_context(context):

	stock_entries = frappe.get_all('Stock Entry',filters={},fields=['name','creation','purpose','posting_date','posting_time','title'])
	for idx,item in enumerate(stock_entries):
		entry = frappe.get_doc('Stock Entry',item.name)
		if entry.items:
			stock_entries[idx]["items"] = entry.items
	print(stock_entries)
	print("done")

	print("get doc test")
	stock_entry = frappe.get_doc('Stock Entry','STE-00001')
	pp.pprint( stock_entry.__dict__ )
	print("stock Entry")
	pp.pprint( stock_entry.items[0].__dict__)



	header = api.get_header()

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

	context["header"] = header
	context["page"] = page
	context["name"] = "packaging"

	context.data = "test data 2"
	return context