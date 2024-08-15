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