# Copyright (c) 2024, JinsoRaj and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class AppUser(Document):
	pass

def add_as_appuser(doc, method):
	if doc.workflow_state == "Approved":
		if not frappe.db.exists("AppUser", doc.name):
			app_user = frappe.new_doc("AppUser")
			app_user.full_name = doc.full_name
			app_user.user_details = doc.name
			app_user.insert(ignore_permissions=True)