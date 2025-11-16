# Copyright (c) 2024, JinsoRaj and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime
import math


class ClassSession(Document):
   pass
	#commenting this beacuse we agreed to take the hours from the volunteer itself instead of auto calculating the hours.
	# def before_save(self):
	# 	if self.session_start_time and self.session_end_time:
	# 		start = get_datetime(self.session_start_time)
	# 		end = get_datetime(self.session_end_time)

	# 		# Calculate difference in hours
	# 		time_diff = (end - start).total_seconds() / 3600

	# 		# Round up to nearest integer, minimum 1
	# 		self.session_total_time = max(1, math.ceil(time_diff))
