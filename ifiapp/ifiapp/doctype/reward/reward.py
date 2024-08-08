# Copyright (c) 2024, JinsoRaj and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Reward(Document):
    
	def before_save(self):
		ifi_id = self.ifi_id
		app_user = frappe.db.get_value("AppUser", {"ifi_id": ifi_id},"name")
		self.app_user = app_user
		if self.app_user == None:
			frappe.throw("No such IFI ID")