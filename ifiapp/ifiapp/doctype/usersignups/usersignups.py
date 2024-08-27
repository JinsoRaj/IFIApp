# Copyright (c) 2024, JinsoRaj and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class UserSignups(Document):
	def before_save(self):
		email_id = self.email_id
		app_user_full_name = frappe.db.get_value("User", {"email": email_id},"full_name")
		self.full_name = app_user_full_name
