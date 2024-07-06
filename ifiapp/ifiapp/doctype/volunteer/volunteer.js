// Copyright (c) 2024, JinsoRaj and contributors
// For license information, please see license.txt

frappe.ui.form.on('Volunteer', {
	refresh: function(frm) {
		frm.set_query("student","students_list", function() {
			return {
				"filters": {
					"school_district": frm.doc.district
				}
			};
		});
	}
});

// frappe.ui.form.on("Volunteer", "onload", function(frm) {
//     frm.set_query("student","students_list", function() {
//         return {
//             "filters": {
//                 "school_name": "Free"
//             }
//         };
//     });
// });

