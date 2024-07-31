# Copyright (c) 2024, JinsoRaj and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Attendance(Document):
	pass



def submit_attendance(attendance_data):
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
        #frappe.db.begin()

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

    except Exception as e:
        # Rollback the transaction if any error occurs
        frappe.db.rollback()
        #frappe.log_error(frappe.get_traceback(), "Attendance Submission Failed")
        #raise frappe.ValidationError("Attendance submission failed. Please try again later.")

# Example usage:
attendance_data = [
    {'student_id': 'S001', 'is_present': 1, 'is_absent': 0},
    {'student_id': 'S002', 'is_present': 0, 'is_absent': 1},
    # Add more records as needed
]

#submit_attendance(attendance_data)
