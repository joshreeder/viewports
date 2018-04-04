from __future__ import unicode_literals
import datetime
import frappe
import frappe.defaults
import pprint

from Page import Page

pp = pprint.PrettyPrinter(indent=4)

class SubAssembly(Page):

	def get_header(self):

		
		res = self.get_sub_assemblies()

		pp.pprint(res)

		completed = sum([res[key]['packed'] for key in res])
		total = sum([res[key]['total'] for key in res])

		now = datetime.datetime.now()
		percent_complete = self.percent_complete(completed,total)

		header = {
			"daily_average": self.get_average("trimmed_actual"),
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

	def get_page(self):
		context = {}
		item = {}

		res = self.get_sub_assemblies()


		item["name"] = "red fillets"
		item["bins"] = {"completed":12,"total":18}

		context["items"] = []

		for key in res:
			obj = {}
			obj['name'] = key
			obj['bins'] = {}
			obj['bins']['completed'] = round(float(res[key]['packed']) / 25)
			obj['bins']['total'] = round(float(res[key]['total']) / 25)
			context['items'].append(obj)

		return context






