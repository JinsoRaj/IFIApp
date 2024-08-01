# Copyright (c) 2024, JinsoRaj and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Attendance(Document):
	pass


attendance_data = [
    {'student_id': 'STUD-2024-00001', 'is_present': 'True'},
    {'student_id': 'STUD-2024-00002', 'is_present': 'True'}
    # Add more records as needed
]

@frappe.whitelist()
def submit_attendance():
    """
    Submit attendance for a list of students. Each entry in `attendance_data` is expected to be
    a dictionary with keys: 'student_id', 'is_present', and 'is_absent'.

    Args:
        attendance_data (list of dict): List of attendance records to be submitted.
    
    Raises:
        frappe.ValidationError: If any attendance record fails to be created, an error will be raised.
    """
    try:
        # Start a new database transaction
        frappe.db.begin()

        for record in attendance_data:
            student_id = record.get('student_id')
            is_present = record.get('is_present')

            # Create a new Attendance document
            attendance_doc = frappe.get_doc({
                'doctype': 'Attendance',
                'student_id': student_id,
                'is_present': is_present
            })

            # Insert the document into the database
            attendance_doc.insert(ignore_permissions=True)

        # Commit the transaction if all records are inserted successfully
        frappe.db.commit()
        return {
             "status": 1,
             "info": "Bulk Attendance marked"
		}

    except Exception as e:
        # Rollback the transaction if any error occurs
        frappe.db.rollback()
        frappe.log_error(frappe.get_traceback(), "Attendance Submission Failed")
        response = {
            "status": 0,
            "info": "Bulk Attendance failed"
        }
        
        # Send a custom error response
        return response
    
        #frappe.log_error(frappe.get_traceback(), "Attendance Submission Failed")
        #raise frappe.ValidationError("Attendance submission failed. Please try again later.")
        
#submit_attendance(attendance_data)
