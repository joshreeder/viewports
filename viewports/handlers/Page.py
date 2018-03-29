
import datetime

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
