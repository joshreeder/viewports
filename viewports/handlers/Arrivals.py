from __future__ import unicode_literals
import datetime
import frappe
import frappe.defaults
import pprint

from Page import Page

pp = pprint.PrettyPrinter(indent=4)

class Arrivals(Page):
	def get_header(self):

		transfers = self.get_transfers()

		complete = sum([item['received'] for item in transfers])
		total = sum([item['expected'] for item in transfers])

		percent_complete = self.percent_complete(complete,total)

		now = datetime.datetime.now()
		header = {
			"daily_average": self.get_average("transfer_actual"),
			"weekday":now.strftime("%A"),
			"date":now.strftime("%b. %d"),
			"time": now.strftime("%H:%M"),
			"pounds_today": {
				"packed": complete,
				"total":total
			},
			"percent_complete":percent_complete,
			"speed":"3,800"

		}
		return header

	def get_page(self):
		harvs = frappe.get_all('Harvest Request', fields=["*"])
		harvs = [item for item in harvs if item['harvest_date'] == self.tdate]

		harvests = {}
		for harv in harvs:
			harv_doc = frappe.get_doc('Harvest Request',harv['name'])
			harv = harv_doc.__dict__
			fish = harv["name"]
			if harvests.get(fish) is not None:
				harvests[fish]["expected"] += int(harv["weight"])
			else:
				harvests[fish] = {
					"expected": int(harv["weight"]),
					"received": 0,
					"fish": harv["fish"],
					"time": harv["harvest_time"]
				}

		harvs = frappe.get_all('Harvest', fields=["*"])
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
			if percent_complete > 1:
				percent_complete = 1
			percent_complete = percent_complete*100
			percent_complete = str(percent_complete)
			harvests[key]["percent_complete"] = percent_complete
			harv_list.append(harvests[key])

		tran_list = self.get_transfers()





		return {"harvests":harv_list,"transfers":tran_list}

	def get_transfers(self):
		#Get transfers
		transfers = frappe.get_all('Fish Transfer Request', 
			fields=["*"],
			filters={"date":self.tdate})
		#transfers = [item for item in transfers if item['date'] == self.tdate]

		tran_obj = {}
		for tran in transfers:
			tran_doc = frappe.get_doc('Fish Transfer Request',tran['name'])
			tran = tran_doc.__dict__

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

		transfers = frappe.get_all('Fish Transfer', fields=["*"])
		transfers = [item for item in transfers if item['date'] == self.tdate]
		for tran in transfers:
			tran_doc = frappe.get_doc('Fish Transfer',tran['name'])
			tran = tran_doc.__dict__
			tran_obj[tran['request']]["received"] += int(tran['weight'])
			tran_obj[tran['request']]["time"] = tran["time"]
		

		tran_list = [tran_obj[key] for key in tran_obj if tran_obj[key]["received"] > 0]

		for idx,item in enumerate(tran_list):
			tran_list[idx]["percent_complete"] = int((float(item["received"]) / float(item["expected"])) * 100)

		return tran_list
