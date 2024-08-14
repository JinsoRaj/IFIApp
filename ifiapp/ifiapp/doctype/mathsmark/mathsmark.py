# Copyright (c) 2024, JinsoRaj and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MathsMark(Document):
	pass


# @frappe.whitelist()
# def create_maths_mark_entry(student_id, topic_id, initial_test_mark, initial_total_mark, final_test_mark, final_total_mark):
#     # Construct the document name
#     doc_name = f"{student_id}-1-{topic_id}"
    
#     # Create the child table entry
#     maths_mark = frappe.get_doc({
#         "doctype": "MathsMark",
#         "name": doc_name,
#         "parent": student_id,
#         "parentfield": "maths_marks",
#         "parenttype": "Student",
#         "topic": topic_id,
#         "initial_test_mark": initial_test_mark,
#         "initial_total_mark": initial_total_mark,
#         "final_test_mark": final_test_mark,
#         "final_total_mark": final_total_mark
#     })
    
#     # Insert the child table entry into the parent document
#     maths_mark.insert(ignore_permissions=True)
#     frappe.db.commit()

#     return {"status": "success", "message": "MathsMark entry created successfully", "doc_name": doc_name}



# @frappe.whitelist()
# def create_or_update_maths_mark_entry(student_id, topic_id, initial_test_mark=-1, initial_total_mark=-1, final_test_mark=-1, final_total_mark=-1):
#     # Construct the document name
#     doc_name = f"{student_id}-1-{topic_id}"
    
#     # Check if an entry for this student and topic already exists
#     if frappe.db.exists("MathsMark", {"parent": student_id, "topic": topic_id}):
#         # Fetch the existing document
#         maths_mark = frappe.get_doc("MathsMark", {"parent": student_id, "topic": topic_id})
        
#         # Update the initial or final marks based on provided input (if they are not -1)
#         if initial_test_mark != -1 and initial_total_mark != -1:
#             maths_mark.initial_test_mark = initial_test_mark
#             maths_mark.initial_total_mark = initial_total_mark
        
#         if final_test_mark != -1 and final_total_mark != -1:
#             maths_mark.final_test_mark = final_test_mark
#             maths_mark.final_total_mark = final_total_mark
        
#         maths_mark.save(ignore_permissions=True)
#         message = "MathsMark entry updated successfully"
#     else:
#         # If no entry exists, create a new entry
#         maths_mark = frappe.get_doc({
#             "doctype": "MathsMark",
#             "name": doc_name,
#             "parent": student_id,
#             "parentfield": "maths_marks",
#             "parenttype": "Student",
#             "topic": topic_id,
#             "initial_test_mark": initial_test_mark if initial_test_mark != -1 else -1,
#             "initial_total_mark": initial_total_mark if initial_total_mark != -1 else -1,
#             "final_test_mark": final_test_mark if final_test_mark != -1 else -1,
#             "final_total_mark": final_total_mark if final_total_mark != -1 else -1,
#         })
        
#         maths_mark.insert(ignore_permissions=True)
#         message = "MathsMark entry created successfully"

#     frappe.db.commit()

#     return {"status": "success", "message": message, "doc_name": maths_mark.name}


#testing bulk maths marks

@frappe.whitelist()
def bulk_create_or_update_maths_mark_entries(maths_marks):
    # Extract topic and total marks from the request
    topic_id = maths_marks.get("topic")
    initial_total_mark = maths_marks.get("initial_total_mark", -1)
    final_total_mark = maths_marks.get("final_total_mark", -1)
    marks_list = maths_marks.get("marks_list", [])

    # Start a new transaction
    frappe.db.begin()

    try:
        # Iterate over each student's marks entry
        for record in marks_list:
            student_id = record.get("student_id")
            initial_test_mark = record.get("initial_test_mark", -1)
            final_test_mark = record.get("final_test_mark", -1)

            # Construct the document name
            doc_name = f"{student_id}-1-{topic_id}"

            # Check if an entry for this student and topic already exists
            if frappe.db.exists("MathsMark", {"parent": student_id, "topic": topic_id}):
                # Fetch the existing document
                maths_mark = frappe.get_doc("MathsMark", {"parent": student_id, "topic": topic_id})
                
                # Update the marks based on provided input
                if initial_test_mark != -1:
                    maths_mark.initial_test_mark = initial_test_mark
                    maths_mark.initial_total_mark = initial_total_mark
                
                if final_test_mark != -1:
                    maths_mark.final_test_mark = final_test_mark
                    maths_mark.final_total_mark = final_total_mark
                
                maths_mark.save(ignore_permissions=True)
            else:
                # If no entry exists, create a new entry
                maths_mark = frappe.get_doc({
                    "doctype": "MathsMark",
                    "name": doc_name,
                    "parent": student_id,
                    "parentfield": "maths_marks",
                    "parenttype": "Student",
                    "topic": topic_id,
                    "initial_test_mark": initial_test_mark if initial_test_mark != -1 else -1,
                    "initial_total_mark": initial_total_mark if initial_total_mark != -1 else -1,
                    "final_test_mark": final_test_mark if final_test_mark != -1 else -1,
                    "final_total_mark": final_total_mark if final_total_mark != -1 else -1,
                })
                
                maths_mark.insert(ignore_permissions=True)

        # Commit the transaction if all records are processed successfully
        frappe.db.commit()
        return {
            "status": "success",
            "message": "Bulk MathsMark entries processed successfully"
        }

    except Exception as e:
        # Rollback the transaction in case of an error
        frappe.db.rollback()
        frappe.log_error(frappe.get_traceback(), "Bulk MathsMark Entry Failed")
        return {
            "status": "error",
            "message": "Bulk MathsMark processing failed",
            "error": str(e)
        }
