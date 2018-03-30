from __future__ import unicode_literals
import datetime
import frappe
import frappe.defaults
import pprint

from Page import Page

pp = pprint.PrettyPrinter(indent=4)

class Packing(Page):

	def get_header(self):
		sales_orders = frappe.get_all("Sales Order", fields=["*"])
		sales_orders = [item for item in sales_orders if item['delivery_date'] == self.tdate]

		harv_reqs = frappe.get_all("Harvest Request", fields=["*"])
		harv_reqs = [item for item in harv_reqs if item['harvest_date'] == self.tdate]

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

	def get_page(self):
		sales_orders = frappe.get_all('Sales Order', fields=["*"])
		sales_orders = [item for item in sales_orders if item['delivery_date'] == self.tdate]

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