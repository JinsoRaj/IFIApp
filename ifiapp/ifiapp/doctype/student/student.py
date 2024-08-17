# Copyright (c) 2024, JinsoRaj and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class Student(Document):
	pass


@frappe.whitelist()
def add_student(**kwargs):
    try:
        # Extract the rewards array from kwargs
        skills = kwargs.get('skills', [])
        
        # Prepare a dictionary to hold the reward fields
        student_data = {}
        
        # Parse the rewards array into individual fields
        for skill in skills:
            for key, value in skill.items():
                student_data[key] = value

        # Merge reward_data back with other kwargs to create the document
        new_student = frappe.get_doc({
            'doctype': 'Student',
            **kwargs,            # Include all other fields
            **student_data        # Add the parsed reward fields
        })
        new_student.insert()
        frappe.db.commit()

        return {'status': 'success', 'message_text': 'Student added successfully.'}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in adding student")
        return {'status': 'error', 'message_text': str(e)}


# update the attendance to student data
def change_total_attendance(doc, method):
		
	#if doc.has_value_changed("roles"):
		if frappe.db.exists("Student", doc.student_id):
			#frappe.msgprint("hello");
			#get the particular student parent doc
			student = frappe.get_doc("Student", doc.student_id)
			#get all attendnce of this student
			full_attendance = frappe.get_all("Attendance",filters={'student_id': doc.student_id},fields=['name','is_present','date'],page_length=365)
			total_entries = len(full_attendance)
			count_present = 0
			
			# Loop through the attendance entries
			for entry in full_attendance:
				if entry['is_present'] == 'True':
					count_present += 1

			attendance_percentage = (count_present / total_entries) * 100
			student.total_attendance = round(attendance_percentage, 2)
			student.flags.ignore_permissions = True
			student.save()
			#frappe.msgprint("<pre>{}</pre>".format(frappe.as_json(attendance_percentage)))
                     
@frappe.whitelist()
def get_student_details(student_id):
    try:
        # Fetch the Student document using the provided student_id
        student_doc = frappe.get_doc("Student", student_id)
        
        # Convert the document to a dictionary format
        student_data = student_doc.as_dict()

        # Define the list of skill fields
        skill_fields = [
            "visual_spatial", "linguistic_verbal", "interpersonal", 
            "intrapersonal", "logical_mathematical", "musical", 
            "bodily_kinesthetic", "naturalistic"
        ]

        # Collect fields with value 1 into the skills array
        skills = [field for field in skill_fields if student_data.get(field) == 1]

        # Add the skills array to the student data
        student_data["skills"] = skills

        # Remove all skill fields from the response
        for field in skill_fields:
            student_data.pop(field, None)

        # Set the data object with the student details
        frappe.response["data"] = student_data
        
        # Set HTTP status code to 200 OK for a successful response
        frappe.response['http_status_code'] = 200

    except frappe.DoesNotExistError:
        # Set HTTP status code to 404 Not Found if the student document does not exist
        frappe.response['http_status_code'] = 404
        frappe.response["message"] = "Student not found."
    except Exception as e:
        # Set HTTP status code to 500 Internal Server Error for any other exceptions
        frappe.response['http_status_code'] = 500
        frappe.log_error(frappe.get_traceback(), "Error in retrieving student details")
        frappe.response["message"] = str(e)