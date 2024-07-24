// Copyright (c) 2024, JinsoRaj and contributors
// For license information, please see license.txt

// frappe.ui.form.on("AppUser", {
// 	refresh(frm) {

// 	},
// });

//todo fix?
frappe.ui.form.on('AppUser', {
	// district: function(frm) {
        
        //get details of selected volunteer user
        // frappe.db.get_value("UserSignups", {"name": frm.doc.user_details}, ["district"])
        // .then(response => {
        //     var district = response.message.district;
        //     //console.log(district);
        //     //limit the students list from same district
        //     frm.set_query("student","students_list", function() {
        //         return {
        //             "filters": {
        //                 "school_district": district
        //             }
        //         };
        //     });
        // })
        // .catch(err => {
        //     console.log(err);
        // });
        
	// },
    onload: function(frm) {
        var full_name = frm.doc.full_name
        var user_link = `/app/user/${frm.doc.name}`
        frm.set_intro(__("To assign roles to {0}, <a href='{1}'> Click here </a>  and change roles of this User from 2nd Tab:    <a href='{1}'>ROLES</a>", [full_name, user_link]), "green");

        frm.set_query("student","students_list", function() {
            return {
                "filters": {
                    "school_district": frm.doc.district
                }
            };
        });
    }
});

// adding vol id/ifi-id in appuser client side 
frappe.ui.form.on("Students", {
    student: function (frm, cdt, cdn) {
        var student = locals[cdt][cdn];
        student.vol_id = cur_frm.doc.ifi_id;
        cur_frm.refresh_field("students_list");
 }
});