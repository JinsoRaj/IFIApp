app_name = "ifiapp"
app_title = "IFIApp"
app_publisher = "JinsoRaj"
app_description = "Flutter Frappe App for Insight for innovation"
app_email = "jinsoraj2000@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ifiapp/css/ifiapp.css"
# app_include_js = "/assets/ifiapp/js/ifiapp.js"

# include js, css files in header of web template
# web_include_css = "/assets/ifiapp/css/ifiapp.css"
# web_include_js = "/assets/ifiapp/js/ifiapp.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ifiapp/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "ifiapp.utils.jinja_methods",
# 	"filters": "ifiapp.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "ifiapp.install.before_install"
# after_install = "ifiapp.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "ifiapp.uninstall.before_uninstall"
# after_uninstall = "ifiapp.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "ifiapp.utils.before_app_install"
# after_app_install = "ifiapp.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "ifiapp.utils.before_app_uninstall"
# after_app_uninstall = "ifiapp.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ifiapp.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ifiapp.tasks.all"
# 	],
# 	"daily": [
# 		"ifiapp.tasks.daily"
# 	],
# 	"hourly": [
# 		"ifiapp.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ifiapp.tasks.weekly"
# 	],
# 	"monthly": [
# 		"ifiapp.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "ifiapp.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ifiapp.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ifiapp.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["ifiapp.utils.before_request"]
# after_request = ["ifiapp.utils.after_request"]

# Job Events
# ----------
# before_job = ["ifiapp.utils.before_job"]
# after_job = ["ifiapp.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"ifiapp.auth.validate"
# ]

fixtures = ["Topic", "IFIModule",{
  'dt': 'Role', 'filters': {'name': ('in', ('Volunteer','Coordinator','Quality Assurance','ifiuser'))},
  'dt': 'Role Profile', 'filters': {'name': ('in', ('ifi'))},
  'dt': 'Workflow', 'filters': {'name': ('in', ('UserApproval'))},
  'dt': 'Workflow State', 'filters': {'name': ('in', ('Draft', 'Approval Pending'))},
  'dt': 'Class', 'filters': {'name': ('in', ('6', '7', '8', '9', '10'))}
}]


doc_events = {
    "UserSignups": {
        "on_update": "ifiapp.ifiapp.doctype.appuser.appuser.add_as_appuser"
    },
    "User": {
        "on_update": "ifiapp.ifiapp.doctype.appuser.appuser.add_roles_in_appuser"
    },
    "Attendance":{
        # "after_insert": "ifiapp.ifiapp.doctype.student.student.change_total_attendance",
        "on_update": "ifiapp.ifiapp.doctype.student.student.change_total_attendance"
    }
}