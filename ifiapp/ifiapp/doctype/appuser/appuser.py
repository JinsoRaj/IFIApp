# Copyright (c) 2024, JinsoRaj and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class AppUser(Document):
	pass

# add approved user signup forms as appusers
def add_as_appuser(doc, method):
	if doc.workflow_state == "Approved":
		if not frappe.db.exists("AppUser", doc.name):
			app_user = frappe.new_doc("AppUser")
			app_user.full_name = doc.full_name
			app_user.user_details = doc.name
			app_user.insert(ignore_permissions=True)

			# create user permission for those approved users in District list
			frappe.get_doc(
			doctype="User Permission",
			user=doc.name,
			allow="Districts",
			for_value=doc.district,
			is_default=0,
			apply_to_all_doctypes=1,
		).insert(ignore_permissions=True)


# update the changes in User roles to appuser roles
def add_roles_in_appuser(doc, method):
	#if doc.has_value_changed("roles"):
		if frappe.db.exists("AppUser", doc.name):
			app_user = frappe.get_doc("AppUser", doc.name)
			user_doc_roles = frappe.get_roles(doc.name)
			app_user.is_volunteer = app_user.is_coordinator = app_user.is_qa = 0

			for role in user_doc_roles:
				if role == "Volunteer":
					app_user.is_volunteer = 1
				elif role == "Coordinator":
					app_user.is_coordinator = 1
				elif role == "Quality Assurance":
					app_user.is_qa = 1
			app_user.flags.ignore_permissions = True
			app_user.save()