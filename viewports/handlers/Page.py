
from __future__ import unicode_literals
import datetime
import frappe
import frappe.defaults
import pprint

pp = pprint.PrettyPrinter(indent=4)

class Page:

	def __init__(self):
		#self.tdate = datetime.datetime.now().date()
		self.tdate = datetime.datetime.strptime('11192018', "%d%m%Y").date()

	def get_page(self):
		return {'message': 'Dummy handle function, overload me!'}
	def get_header(self):
		return {'message': 'Dummy handle function, overload me!'}

	def get_daily_reports(self):
		daily_reports = frappe.get_all("Processing Plant Daily Report Temp", fields=["*"])
		return daily_reports

	def get_average(self,key):
		total = 0
		count = 0
		drs = self.get_daily_reports()
		for report in drs:
			if report.get(key) != None:
				total += int(report.get(key))
				count += 1

		if count < 1:
			count = 1
		avg = float(total) / float(count)
		return avg

	def get_record(self,key):
		record = 0.0
		drs = self.get_daily_reports()
		for report in drs:
			if report.get(key) != None:
				chal = float(report.get(key))
				if chal > record:
					record = chal
		return record


	def get_announcements(self):

		rooms = frappe.get_all('Chat Room', fields=["*"])
		rooms = [item['name'] for item in rooms if 'announcement' in item['room_name'].lower()]

		messages = frappe.get_all('Chat Message', fields=["*"])
		messages = [item for item in messages if item['room'] in rooms]

		messages = sorted(messages, key=lambda k: k['creation'], reverse=True)

		messages = [item['content'] for item in messages]

		return messages

	def get_data(self):
		return {
			"header":self.get_header(),
			"page":self.get_page(),
			"announcements":self.get_announcements()
		}
	def percent_complete(self,a,b):
		if b == 0:
			if a > 0:
				return "100%"
			return "0%"
		percent_complete = ( float(a)/float(b) ) * 100
		percent_complete = str(int(percent_complete)) + "%"
		return percent_complete

	def get_packaging_requests(self):
		sales_orders = frappe.get_all("Sales Order",
			fields=["name"],
			filters={"delivery_date":self.tdate})

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
		filters = {
			"posting_date":self.tdate
		}
		if filter_by is not None:
			filters["purpose"] = filter_by
		entries = frappe.get_all("Stock Entry",
			fields=["name"],
			filters=filters)

		res = []
		groups = {}
		for entry in entries:
			doc = frappe.get_doc('Stock Entry',entry['name'])
			doc = doc.__dict__
			items = doc["items"]
			for item in items:
				entry = item.__dict__
				group = entry["item_code"]
				item = frappe.get_doc('Item',entry["item_code"]).__dict__
				if groups.get(group) is not None:
					groups[group]['qty'] += entry["qty"]
				else:
					groups[group] = {}
					groups[group]['qty'] = entry["qty"]
					if item['weight_per_unit'] != None:
						groups[group]['weight_per_unit'] = item['weight_per_unit']
					else:
						groups[group]['weight_per_unit'] = 1.0


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
				res[key]['packed'] += entries[key]['qty']

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

	def separate_oz(self,item_code):
		idx = item_code.upper().index("OZ")
		res = {}
		res["name"] = item_code[idx+3:]
		res["oz"] = item_code[:idx]
		return res
