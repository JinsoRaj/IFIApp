import frappe
from datetime import timedelta
from frappe.auth import LoginManager
from frappe.website.utils import is_signup_disabled
from frappe.utils import random_string
from frappe import DoesNotExistError
from frappe.utils import (
	cint,
	escape_html,
	flt,
	format_datetime,
	get_formatted_email,
	get_system_timezone,
	has_gravatar,
	now_datetime,
	today,
)
import frappe.defaults
import frappe.permissions
import frappe.share
import random

#import frappe.cache

@frappe.whitelist(allow_guest=True)

#test ping
def ping():
	number = random.randint(1000,9999)
	print(number)
	return number

#send mails for email verification
def send_email(email_address,number_code):
    frappe.sendmail(recipients=email_address,
		subject="IFI Mail verification code",
		message= number_code)

#signup function - used to register the user in backend. bydefault the user is disabled and wont be able to login. Once the email is verified, the user is enabled and allowed to login.
@frappe.whitelist(allow_guest=True)
def sign_up(email: str, password: str, full_name: str, redirect_to: str) -> tuple[int, str]:
	# if signup is disabled from website settings
	if is_signup_disabled():
		frappe.throw(("Sign Up is disabled"), title=("Not Allowed"))

	user = frappe.db.get("User", {"email": email})
	if user:
		if user.enabled:
			return 0, ("Already Registered")
		else:
			return 0, ("Registered but disabled")
	else:
		if frappe.db.get_creation_count("User", 60) > 300:
			frappe.respond_as_web_page(
						("Temporarily Disabled"),
						(
							"Too many users signed up recently, so the registration is disabled. Please try back in an hour"
						),
						http_status_code=429,
					)
		
	user = frappe.get_doc(
		{
				"doctype": "User",
				"email": email,
				"first_name": escape_html(full_name),
				"enabled": 0,
				"new_password": password,
				"user_type": "Website User",
				"send_welcome_email": 0
		}
		)
	user.flags.ignore_permissions = True
	user.flags.ignore_password_policy = True
	#send a mail
	#generate 4 digit key
	number_code = random.randint(1000,9999)
	#store key in reset_password_key
	user.db_set("reset_password_key", number_code)

	#store time of generation in last_reset_password_key_generated_on
	current_datetime = now_datetime()
	user.db_set("last_reset_password_key_generated_on", current_datetime)
	#store the time limit in reset_password_link_expiry system settings = 30min
	
	#create disabled user 
	user.insert()

	#print(frappe.local.response)
	#remove the not found execption from user.insert(). idk why
	#if frappe.local.response["exc_type"] == "DoesNotExistError":
		#frappe.local.response.pop("exc_type")

	#send code to user via mail
	send_email(email,number_code)
	# set default signup role as per Portal Settings
	#default_role = frappe.db.get_single_value("Portal Settings", "default_role")
	#if default_role:
		#user.add_roles(default_role)
		
	return 1, "Created user"

@frappe.whitelist(allow_guest=True)
def verify_mail(email: str, number_code: str):
	#user = frappe.db.get("User", {"email": email})
	user = frappe.get_doc("User", email)
	#user.flags.ignore_permissions = True
	#print(user)
	#user.db_set("reset_password_key", number_code)
	user.flags.ignore_permissions = True
	stored_code = user.reset_password_key
	last_reset_password_key_generated_on = user.last_reset_password_key_generated_on
	reset_password_link_expiry = cint(
				frappe.get_system_settings("reset_password_link_expiry_duration")
			)
	
	#expired when - now_datetime() > last_reset_password_key_generated_on + timedelta(seconds=reset_password_link_expiry)
	#if not expired - then match usercode with stored key, if same enable the user and save.
	if now_datetime() < last_reset_password_key_generated_on + timedelta(seconds=reset_password_link_expiry):
		if number_code == stored_code:
			user.enabled = 1
			user.save()
			frappe.db.commit()
			return 1, "Verified"
	#user.reset_password_key = number_code
	#user.last_name = "nys"
	 
	#key = user.reset_password_key
	return 0, "Mail not verified"

@frappe.whitelist(allow_guest = True)
def app_login(usr,pwd):
	login_manager = LoginManager()
	login_manager.authenticate(usr,pwd)
	login_manager.post_login()
	if frappe.response['message'] == 'Logged In':
		user = login_manager.user
		frappe.response['key_details'] = generate_key(user)
		frappe.response['user_details'] = get_user_details(user)
	else:
		return False
	
def generate_key(user):
	user_details = frappe.get_doc("User", user)
	api_secret = api_key = ''
	if not user_details.api_key and not user_details.api_secret:
		api_secret = frappe.generate_hash(length=15)
		api_key = frappe.generate_hash(length=15)
		user_details.api_key = api_key
		user_details.api_secret = api_secret
		user_details.save(ignore_permissions = True)
	else:
		api_secret = user_details.get_password('api_secret')
		api_key = user_details.get('api_key')
	return {"api_secret": api_secret,"api_key": api_key}

def get_user_details(user):
	user_details = frappe.get_all("User",filters={"name":user},fields=["name","first_name","last_name","email","mobile_no","gender","role_profile_name"])
	if user_details:
		return user_details