// Copyright (c) 2024, JinsoRaj and contributors
// For license information, please see license.txt

// frappe.ui.form.on("AppUser", {
// 	refresh(frm) {

// 	},
// });

//todo fix?
frappe.ui.form.on('AppUser', {
	user_details: function(frm) {
        //get details of selected volunteer user
        frappe.db.get_value("UserSignups", {"name": frm.doc.user_details}, ["district"])
        .then(response => {
            var district = response.message.district;
            //console.log(district);
            //limit the students list from same district
            frm.set_query("student","students_list", function() {
                return {
                    "filters": {
                        "school_district": district
                    }
                };
            });
        })
        .catch(err => {
            console.log(err);
        });
        
        
		// frm.set_query("student","students_list", function() {
		// 	return {
		// 		"filters": {
		// 			"school_district": fl_name
		// 		}
		// 	};
		// });
	}
});