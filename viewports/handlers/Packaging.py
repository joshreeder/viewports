
import datetime
import frappe
import frappe.defaults
import pprint

from .Page import Page

pp = pprint.PrettyPrinter(indent=4)

class Packaging(Page):

	def get_header(self):

		try:

			products = self.get_production_items()
			completed = sum([products[key]['completed'] * products[key]['weight_per_unit'] for key in products])
			total = sum([products[key]['total'] * products[key]['weight_per_unit'] for key in products])

			now = datetime.datetime.now()
			percent_complete = self.percent_complete(completed,total)

			header = {
				"daily_average": self.get_average("shipped_actual"),
				"weekday":now.strftime("%A"),
				"date":now.strftime("%b. %d"),
				"time": now.strftime("%H:%M"),
				"pounds_today": {
					"packed": completed,
					"total":total
				},
				"percent_complete":percent_complete,
				"speed":"3,800"

			}

			return header

		except Exception as ex:
			print(ex)

	def get_page(self):

		products = self.get_production_items()
		products = [products[key] for key in products]

		page = {
			"products":products
		}

		return page

	def get_production_items(self):

		try:
			sales_orders = frappe.get_all('Sales Order', fields=["*"])
			sales_orders = [item for item in sales_orders if item['delivery_date'] == self.tdate]

			item_codes = {}
			for so in sales_orders:
				so_doc = frappe.get_doc('Sales Order',so['name'])
				for item in so_doc.items:
					item = item.__dict__
					item_code = item.get("item_code")
					if item_codes.get(item_code) is not None:
						item_codes[item_code]["total"] += item["qty"]
					else:
						item_doc = frappe.get_doc('Item',item_code).__dict__
						item_codes[item_code] = {}

						sep_oz = self.separate_oz(item_code)

						item_codes[item_code]["total"] = item["qty"]
						item_codes[item_code]["completed"] = 0
						item_codes[item_code]["name"] = sep_oz["name"]
						item_codes[item_code]["oz"] = sep_oz["oz"]
						item_codes[item_code]['weight_per_unit'] = item_doc['weight_per_unit']

			repacks = self.get_stock_entries('Repack')

			for key in item_codes:
				if repacks.get(key) != None:
					item_codes[key]["completed"] = repacks[key]["qty"]

			return item_codes

		except Exception as ex:
			print(ex)
