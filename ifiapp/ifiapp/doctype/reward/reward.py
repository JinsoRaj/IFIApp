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

def increase_points(doc, method):
	result = frappe.get_all(
		"Energy Point Log",
		filters={"user": doc.user, "type": ["!=", "Review"]},
		group_by="type",
		order_by="type",
		fields=["ABS(sum(points)) as points"],
	)
	
	energy_points = result[0]['points']

	frappe.db.set_value("AppUser",doc.user,"points_gained",energy_points)

@frappe.whitelist()
def get_recent_rewards(ifi_id):
	response = {
				"status": "error",
				"info": "No Rewards to show",
				"recent_points": []
			}
	try:
		app_user = frappe.db.get_value("AppUser", {"ifi_id": ifi_id},"name")
		points_list = []
		points_list = frappe.get_all(
			"Energy Point Log",
			filters={"user": app_user},  # Filter by user
			fields=["rule","points"],  # Adjust fields as needed
			limit=5,
			order_by='creation desc'
		)
		if points_list:
			response = {
				"status": "success",
				"info": "Recent Rewards",
				"recent_points": points_list
			}
		return response
	except Exception as e:
		response = {
            "status": "error",
            "info": "Error in showing your rewards!"
        }
		return response
	

@frappe.whitelist()
def add_rewards(**kwargs):
    try:
        # Extract the rewards array from kwargs
        rewards = kwargs.get('rewards', [])
        
        # Prepare a dictionary to hold the reward fields
        reward_data = {}
        
        # Parse the rewards array into individual fields
        for reward in rewards:
            for key, value in reward.items():
                reward_data[key] = value

        # Merge reward_data back with other kwargs to create the document
        new_reward = frappe.get_doc({
            'doctype': 'Reward',
            **kwargs,            # Include all other fields
            **reward_data        # Add the parsed reward fields
        })
        new_reward.insert()
        frappe.db.commit()

        return {'status': 'success', 'message_text': 'Reward added successfully.'}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error adding reward")
        return {'status': 'error', 'message_text': str(e)}