from __future__ import unicode_literals
import datetime
import frappe
import frappe.defaults
import pprint

from Page import Page

pp = pprint.PrettyPrinter(indent=4)

class Packing(Page):

	def get_header(self):
		orders = self.get_sales_orders()

		packed = sum([item['total_packed'] for item in orders]) * 5
		total = sum([item['total_quantity'] for item in orders]) * 5

		percent_complete = self.percent_complete(packed,total)

		now = datetime.datetime.now()
		header = {
			"daily_average": self.get_average("packaged_actual"),
			"weekday":now.strftime("%A"),
			"date":now.strftime("%b. %d"),
			"time": now.strftime("%H:%M"),
			"pounds_today": {
				"packed": packed,
				"total":total
			},
			"percent_complete":percent_complete,
			"speed":"3,800"

		}
		return header

	def get_page(self):
		order_list = self.get_sales_orders()

		return {"orders":order_list}

	def get_sales_orders(self):
		sales_orders = frappe.get_all('Sales Order', fields=["*"])
		sales_orders = [item for item in sales_orders if item['delivery_date'] == self.tdate]

		orders = {}
		for so in sales_orders:
			so_doc = frappe.get_doc('Sales Order',so['name'])
			#pp.pprint(so_doc.__dict__)
			order = {
				"company":so_doc.customer_name,
				"items":{},
				"total_quantity": 0,
				"total_packed": 0
			}
			for item in so_doc.items:
				item = item.__dict__
				item_code = item['item_code']
				order_item = {
					"packed": 0,
					"quantity": int(item['qty']),
					"item_code": item_code,
					"percent_complete": 0
				}
				order["total_quantity"] += int(item['qty'])
				order["items"][item_code] = order_item
			orders[so_doc.customer_name] = order

		delivery_notes = frappe.get_all('Delivery Note', fields=["*"])
		delivery_notes = [item for item in delivery_notes if item['posting_date'] == self.tdate]

		for dn in delivery_notes:
			dn = frappe.get_doc('Delivery Note',dn['name'])
			dn = dn.__dict__
			if orders.get(dn['customer_name']) != None:
				for item in dn["items"]:
					item_code = item.item_code
					if orders[dn['customer_name']]["items"].get(item_code) != None:
						orders[dn['customer_name']]["items"][item_code]["packed"] += item.qty
						orders[dn['customer_name']]["total_packed"] += item.qty

		order_list = []
		for key in orders:
			order = orders[key]
			item_list = []
			for key2 in order['items']:
				item = order['items'][key2]
				item["percent_complete"] = self.percent_complete(item["packed"],item["quantity"])
				item_list.append(item)
			order['items'] = item_list
			#order["percent_complete"] = self.percent_complete(order["total_packed"],order["total_quantity"])
			order_list.append(order)

		pp.pprint(order_list)

		return order_list
