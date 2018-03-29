
from __future__ import unicode_literals
import datetime
import frappe
import frappe.defaults
import pprint

pp = pprint.PrettyPrinter(indent=4)

class Page:

	def __init__(self):
		self.tdate = datetime.datetime.strptime('27032018', "%d%m%Y").date()

	def get_page(self):
		return {'message': 'Dummy handle function, overload me!'}
	def get_header(self):
		return {'message': 'Dummy handle function, overload me!'}
	def get_data(self):
		return {
			"header":self.get_header(),
			"page":self.get_page()
		}
	def percent_complete(self,a,b):
		percent_complete = ( float(a)/float(b) ) * 100
		percent_complete = str(int(percent_complete)) + "%"
		return percent_complete

	def get_packaging_requests(self):
		sales_orders = frappe.get_all("Sales Order", fields=["*"])
		sales_orders = [item for item in sales_orders if item['delivery_date'] == self.tdate]

		groups = {}
		for so in sales_orders:
			so = frappe.get_doc('Sales Order',so['name'])
			so = so.__dict__
			items = so["items"]
			for item in items:
				item = item.__dict__
				group = item["item_code"]
				if groups.get(group) is not None:
					groups[group] += item["total_weight"]
				else:
					groups[group] = item["total_weight"]

		return groups

	def get_stock_entries(self,filter_by=None):
		entries = frappe.get_all("Stock Entry", fields=["*"])
		if filter_by != None:
			entries = [item for item in entries if item['posting_date'] == self.tdate and item['purpose'] == filter_by]

		res = []
		groups = {}
		for entry in entries:
			doc = frappe.get_doc('Stock Entry',entry['name'])
			doc = doc.__dict__
			items = doc["items"]
			for item in items:
				item = item.__dict__
				group = item["item_code"]
				if groups.get(group) is not None:
					groups[group] += item["qty"]
				else:
					groups[group] = item["qty"]

		return groups

	def get_sub_assemblies(self):
		entries = self.get_stock_entries("Manufacture")
		packaging = self.get_packaging_requests()

		material_output = frappe.get_all('Material Output', fields=["*"])

		material_output = [frappe.get_doc('Material Output',item['name']).__dict__ for item in material_output]

		item2sub = {}
		for item in material_output:
			for item2 in item["output_items"]:
				item2 = item2.__dict__
				item2sub[item2['item']] = item2['parent']

		res = {}

		for key in packaging:
			res[item2sub[key]] = {
				"packed": 0,
				"total": packaging[key]
			}


		for key in entries:
			if key in res:
				res[key]['packed'] += entries[key]

		return res

	def lbs2bins(self,lbs):
		bins = int(round(float(lbs) / 25))
		return bins

	def abbrev(self,phrase):
		phrase = phrase.split()
		word = ""
		for item in phrase:
			word += item[0]
		return word
