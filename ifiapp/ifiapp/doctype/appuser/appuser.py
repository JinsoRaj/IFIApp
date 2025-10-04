# Copyright (c) 2024, JinsoRaj and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
import random


class AppUser(Document):
    # def before_save(self):
        # Check if User Permission already exists for this user
        # existing_permissions = frappe.db.exists(
        #     "User Permission", {"user": self.name, "allow": "Districts"}
        # )

        # if existing_permissions:
        #     # Delete all existing User Permissions for this user related to Districts
        #     frappe.db.delete("User Permission", {"user": self.name, "allow": "Districts"})

        # Create new user permission for the current district
        # frappe.get_doc({
        #     "doctype": "User Permission",
        #     "user": self.name,
        #     "allow": "Districts",
        #     "for_value": self.district,  # Assuming `self.district` contains the district field
        #     "is_default": 0,
        #     "apply_to_all_doctypes": 1,
        # }).insert(ignore_permissions=True)


    #validation starts - last change
    def validate(self):
        # Add this new validation method
        self.validate_duplicate_schools()
    
    def validate_duplicate_schools(self):
        """Validate that there are no duplicate schools in the schools table"""
        if not self.get("schools"):
            return
            
        seen_schools = set()
        
        for school in self.schools:
            if school.schools in seen_schools:
                frappe.throw(
                    _(f"School '{school.schools}' is already mapped to this user. Please remove the duplicate entry."),
                    title=_("Duplicate School")
                )
            seen_schools.add(school.schools)

# Rest of your existing code remains exactly the same... validation change ends


# add approved user signup forms as appusers
def add_as_appuser(doc, method):
	if doc.workflow_state == "Approved":
		if not frappe.db.exists("AppUser", doc.name):
			app_user = frappe.new_doc("AppUser")
			app_user.profile_pic = doc.profile_pic
			app_user.full_name = doc.full_name
			app_user.ph_number = doc.ph_number
			app_user.user_details = doc.name
			app_user.gender = doc.gender
			app_user.state = doc.state
			app_user.district = doc.district
			app_user.emp_status = doc.emp_status
			app_user.college_name = doc.college_name
			app_user.res_address = doc.res_address
			random_number = random.randint(100000, 999999)
			app_user.ifi_id = f"IFI-{random_number}"
			app_user.insert(ignore_permissions=True)



# update the changes in User roles to appuser roles
def add_roles_in_appuser(doc, method):
	#if doc.has_value_changed("roles"):
		if frappe.db.exists("AppUser", doc.name):
			app_user = frappe.get_doc("AppUser", doc.name)
			user_doc_roles = frappe.get_roles(doc.name)
			app_user.is_volunteer = app_user.is_coordinator = app_user.is_qa = app_user.is_dis_coordinator = 0

			for role in user_doc_roles:
				if role == "Volunteer":
					app_user.is_volunteer = 1
				elif role == "Coordinator":
					app_user.is_coordinator = 1
				elif role == "Quality Assurance":
					app_user.is_qa = 1
				elif role == "District Coordinator":
					app_user.is_dis_coordinator = 1
			app_user.flags.ignore_permissions = True
			app_user.save()


@frappe.whitelist()
def get_appuser_and_students(ifi_id):
    try:
        # Attempt to fetch the AppUser document
        app_user = frappe.get_doc("AppUser", {"ifi_id": ifi_id})

        # Initialize the list to hold student details
        student_details = []

        # Iterate over the students_list child table
        for student in app_user.students_list:
            # Fetch the linked Student document using the 'student' field from the child table
            student_doc = frappe.get_doc("Student", student.student)
            
            # Add required fields to the result
            student_details.append({
                "student_id": student.student,
                "full_name": student_doc.full_name,
                "school_name": student_doc.school_name,
                "class_name": student_doc.class_name,
                "school_district": student_doc.school_district,
                "grade": student_doc.grade,
            })

        # Prepare the AppUser details
        ifi_user_details = {
            "name": app_user.name,
			"profile_pic": app_user.profile_pic,
            "ifi_id": app_user.ifi_id,
            "full_name": app_user.full_name,
            "gender": app_user.gender,
            "points_gained": app_user.points_gained,
            "is_volunteer": app_user.is_volunteer,
            "is_coordinator": app_user.is_coordinator,
            "is_qa": app_user.is_qa,
            "state": app_user.state,
            "district": app_user.district,
            "user_details": app_user.user_details,
            "res_address": app_user.res_address,
            "doctype": app_user.doctype,
        }

        # If everything is successful, set the response
        frappe.local.response.http_status_code = 200 
      #   frappe.response["message"] = {
      #       "status": "success",
      #       "message_text": "AppUser and student details retrieved successfully."
      #   }
        frappe.response["data"] = {
            "ifi_user_details": ifi_user_details,
            "student_details": student_details
        }

    except frappe.DoesNotExistError:
        # Handle case where the AppUser or Student document doesn't exist
        frappe.local.response.http_status_code = 404
      #   frappe.response["message"] = {
      #       "status": "error",
      #       "message_text": "AppUser or Student not found."
      #   }
        frappe.response["data"] = {}

    except Exception as e:
        # Handle unexpected errors
        frappe.local.response.http_status_code = 500
      #   frappe.response["message"] = {
      #       "status": "error",
      #       "message_text": f"An unexpected error occurred: {str(e)}"
      #   }
        frappe.response["data"] = {}

    finally:
        # Ensure the function returns cleanly
        return