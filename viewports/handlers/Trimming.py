from __future__ import unicode_literals
import datetime
import frappe
import frappe.defaults
import pprint

from Page import Page

pp = pprint.PrettyPrinter(indent=4)

class Trimming(Page):

	def get_header(self):
		res = self.get_sub_assemblies()

		daily_reports = self.get_daily_reports()
		avg = self.get_average("packaged_actual")

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

		trimmers = self.get_trimmer_scores()
		trimmer_objs = []
		for key in trimmers:
			trimmers[key]["bins"] = int(round(float(trimmers[key]["lbs"]) / 25))
			trimmer_objs.append(trimmers[key])
			

		subs = self.get_sub_assemblies()


		context["subs"] = []

		for key in subs:
			obj = {
				"packed":subs[key]['packed'],
				"bins": self.lbs2bins(subs[key]['packed']),
				"abbrev":self.abbrev(key)
			}
			context['subs'].append(obj)


		context["trimmers"] = trimmer_objs

		total_trimmed = sum([item["bins"] for item in trimmer_objs])

		context["trimmed"] = total_trimmed
		context["average"] = float(total_trimmed) / float(len(trimmer_objs))
		context["record"] = self.get_record('trimmed_actual')


		return context

	def get_trimmer_scores(self):

		trimmer_codes = frappe.get_all("Trimmer Code", fields=["*"])

		trimmers = {}

		for item in trimmer_codes:
			trimmers[item["name"]] = {
				"trimmer_number": item["trimmer_number"],
				"lbs": 0
			}

		entries = frappe.get_all("Stock Entry", fields=["*"])
		entries = [item for item in entries if item['posting_date'] == self.tdate and item['purpose'] == 'Manufacture']

		for entry in entries:
			doc = frappe.get_doc('Stock Entry',entry['name'])
			doc = doc.__dict__
			if doc['work_done_by'] != None:
				items = doc["items"]
				for item in items:
					item = item.__dict__
					trimmers[doc['work_done_by']]["lbs"] +=  item["qty"]

		return trimmers
