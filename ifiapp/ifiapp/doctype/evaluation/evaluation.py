# Copyright (c) 2024, JinsoRaj and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Evaluation(Document):
	def before_save(self):
		ifi_id = self.ifi_id
		app_user = frappe.db.get_value("AppUser", {"ifi_id": ifi_id},"name")
		self.volunteer = app_user
		if self.volunteer == None:
			frappe.throw("No such volunteer IFI ID")
                  
		evaluator_id = self.evaluator_id
		app_user = frappe.db.get_value("AppUser", {"ifi_id": evaluator_id},"name")
		self.evaluator = app_user
		if self.evaluator == None:
			frappe.throw("No such evaluator ID")


@frappe.whitelist(allow_guest=True)
def send_evaluation(**kwargs):
    """
    API function to create a new Evaluation record in Frappe using dynamic parameters (kwargs).
    
    Args:
        kwargs (dict): Dynamic key-value pairs for evaluation details.
            Expected keys include:
                - volunteer (str): Name or ID of the volunteer.
                - evaluator (str): Name or ID of the evaluator.
                - date (str): Evaluation date in YYYY-MM-DD format.
                - time (str): Evaluation time in HH:MM format.
                - mode (str): Mode of evaluation (e.g., Online, In-person).
                - questions (list): List of questions with their scores.
                - final_score (float): Final score for the evaluation.
    
    Returns:
        Sets `frappe.response` with status and message.
    """
    try:
        required_fields = ["ifi_id", "evaluator_id"]

        # Validate required fields
        for field in required_fields:
            if field not in kwargs or not kwargs.get(field):
                frappe.response["http_status_code"] = 400  # Bad Request
                frappe.response["status"] = "error"
                frappe.response["message_text"] = f"'{field}' is required."
                return

      # Calculate final_score if table_questions exists
        total_marks = 0
        if "table_questions" in kwargs and isinstance(kwargs["table_questions"], list):
            for question in kwargs["table_questions"]:
                if "mark" in question:
                    total_marks += int(question["mark"])  # Ensure mark is an integer

        # Append final_score to kwargs
        kwargs["final_score"] = total_marks

        # Insert the Evaluation record
        evaluation = frappe.get_doc({
            "doctype": "Evaluation",
            **kwargs  # Dynamically pass all kwargs as fields for the Evaluation
        })
        evaluation.insert(ignore_permissions=True)
        frappe.db.commit()  # Commit to save changes

        # Set success response
        frappe.response["http_status_code"] = 200  # OK
        frappe.response["status"] = "success"
        frappe.response["message_text"] = "Evaluation added successfully."
        frappe.response["evaluation_id"] = evaluation.name  # Add the name of the created record for reference

    except Exception as e:
        # Log error and set failure response
        frappe.log_error(frappe.get_traceback(), "Evaluation Submission Error")
        frappe.response["http_status_code"] = 500  # Internal Server Error
        frappe.response["status"] = "error"
        frappe.response["message_text"] = str(e)