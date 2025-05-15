# Copyright (c) 2024, JinsoRaj and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe import throw, _


class College(Document):
    def validate(self):
        self.validate_duplicate_schools()
    
    def validate_duplicate_schools(self):
        if not self.get("mapped_schools"):
            return
            
        seen_schools = set()
        
        for school in self.mapped_schools:
            if school.schools in seen_schools:
                throw(_(f"School '{school.schools}' is already mapped to this college. Please remove the duplicate entry."))
            seen_schools.add(school.schools)