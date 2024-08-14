# Copyright (c) 2024, JinsoRaj and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EnglishMark(Document):
	pass


@frappe.whitelist()
def bulk_add_or_update_english_marks(english_marks):
    """
    Function to handle bulk addition or update of English marks and grade levels for multiple students.
    It handles one type of test marks and grade levels at a time: initial, intermediate, or final.
    
    Args:
        english_marks (dict): Contains topic, total marks, grade levels, and list of student marks to be processed.
    """
    try:
        data = frappe.parse_json(english_marks)
        topic_id = data.get("topic")
        
        # Determine which type of mark and grade level is being processed
        initial_test_mark = data.get("initial_total_mark", None)
        intermediate_test_mark = data.get("intermediate_total_mark", None)
        final_test_mark = data.get("final_total_mark", None)
        
        for record in data.get("marks_list", []):
            student_id = record.get("student_id")
            doc_name = f"{student_id}-2-{topic_id}"
            
            if frappe.db.exists("EnglishMark", {"parent": student_id, "topic": topic_id}):
                english_mark = frappe.get_doc("EnglishMark", {"parent": student_id, "topic": topic_id})
                
                if initial_test_mark is not None:
                    if record.get("initial_test_mark") is not None:
                        english_mark.initial_test_mark = record.get("initial_test_mark")
                    if initial_test_mark != -1:
                        english_mark.initial_total_mark = initial_test_mark
                    if record.get("initial_grade_level") is not None:
                        english_mark.initial_grade_level = record.get("initial_grade_level")
                
                if intermediate_test_mark is not None:
                    if record.get("intermediate_test_mark") is not None:
                        english_mark.intermediate_test_mark = record.get("intermediate_test_mark")
                    if intermediate_test_mark != -1:
                        english_mark.intermediate_total_mark = intermediate_test_mark
                    if record.get("intermediate_grade_level") is not None:
                        english_mark.intermediate_grade_level = record.get("intermediate_grade_level")
                
                if final_test_mark is not None:
                    if record.get("final_test_mark") is not None:
                        english_mark.final_test_mark = record.get("final_test_mark")
                    if final_test_mark != -1:
                        english_mark.final_total_mark = final_test_mark
                    if record.get("final_grade_level") is not None:
                        english_mark.final_grade_level = record.get("final_grade_level")

                english_mark.save(ignore_permissions=True)
            else:
                english_mark = frappe.get_doc({
                    "doctype": "EnglishMark",
                    "name": doc_name,
                    "parent": student_id,
                    "parentfield": "english_marks",
                    "parenttype": "Student",
                    "topic": topic_id,
                    "initial_test_mark": record.get("initial_test_mark", -1) if initial_test_mark is not None else -1,
                    "initial_total_mark": initial_test_mark if initial_test_mark != -1 else -1,
                    "initial_grade_level": record.get("initial_grade_level") if initial_test_mark is not None else None,
                    "intermediate_test_mark": record.get("intermediate_test_mark", -1) if intermediate_test_mark is not None else -1,
                    "intermediate_total_mark": intermediate_test_mark if intermediate_test_mark != -1 else -1,
                    "intermediate_grade_level": record.get("intermediate_grade_level") if intermediate_test_mark is not None else None,
                    "final_test_mark": record.get("final_test_mark", -1) if final_test_mark is not None else -1,
                    "final_total_mark": final_test_mark if final_test_mark != -1 else -1,
                    "final_grade_level": record.get("final_grade_level") if final_test_mark is not None else None,
                })
                english_mark.insert(ignore_permissions=True)
        
        frappe.db.commit()
        return {"status": "success", "message_text": "Bulk English marks and grades processed successfully."}

    except Exception as e:
        # Rollback the transaction if any error occurs
        frappe.db.rollback()
        frappe.log_error(frappe.get_traceback(), "Bulk English Mark Submission Failed")
        return {"status": "error", "message_text": "Bulk English mark submission failed. Please try again later."}
