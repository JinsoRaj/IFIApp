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
	message = f"""
    Hello,
    Your OTP for verifying your email is: {number_code}

	 Please enter this code in your mobile app to complete your verification.
    Thank you,
    Insight for Innovation Team
    """
	frappe.sendmail(recipients=email_address,
		subject="IFI Mail verification code",
		message= message,
		delayed=False,
		retry=1,)

#signup function - used to register the user in backend. bydefault the user is disabled and wont be able to login. Once the email is verified, the user is enabled and allowed to login.
@frappe.whitelist(allow_guest=True)
def sign_up(email: str, password: str, full_name: str, redirect_to: str):
	# if signup is disabled from website settings
	if is_signup_disabled():
		frappe.throw(("Sign Up is disabled"), title=("Not Allowed"))

	if frappe.db.exists("User", {"email": email}):
		user = frappe.db.get("User", {"email": email})
		if user:
			if user.enabled:
				return {
					"status": 0,
					"message_text": "Already Registered"
					}
			else:
				return {
					"status": 0,
					"message_text": "Registered but disabled"
					}
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
	#generate 6 digit key
	number_code = random.randint(100000,999999)
	#store key in reset_password_key
	user.db_set("reset_password_key", number_code)

	#store time of generation in last_reset_password_key_generated_on
	current_datetime = now_datetime()
	user.db_set("last_reset_password_key_generated_on", current_datetime)
	#user.db_set("role_profile_name","ifi")
	#user.role_profile_name = "ifi"
	#store the time limit in reset_password_link_expiry system settings = 30min
	
	#create disabled user 

	user.insert()
	frappe.db.commit()

	send_email(email,number_code)

	# disable noti settings
	if frappe.db.exists("Notification Settings", email):
		noti = frappe.get_doc("Notification Settings", email)
		noti.enabled = 0
		noti.flags.ignore_permissions = True
		noti.save()
		frappe.db.commit()
	#add write role for guest in desk

	#print(frappe.local.response)
	#remove the not found execption from user.insert(). idk why
	#if frappe.local.response["exc_type"] == "DoesNotExistError":
		#frappe.local.response.pop("exc_type")

	#send code to user via mail
	
	# set default signup role as per Portal Settings
	#default_role = frappe.db.get_single_value("Portal Settings", "default_role")
	#if default_role:
		#user.add_roles(default_role)
	return {
		"status": 1,
		"message_text": "Created user"
		}

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
		noti = frappe.get_doc("Notification Settings", email)
		noti.enabled = 1
		noti.flags.ignore_permissions = True
		noti.save()
		frappe.db.commit()
		
		if number_code == stored_code:
			user.enabled = 1
			#user.role_profile_name = "ifi"
			user.add_roles("ifiuser")
			user.save()
			frappe.db.commit()

			return {
				"status": 1,
				"message_text": "Verified"
				}
	#user.reset_password_key = number_code
	#user.last_name = "nys"
	 
	#key = user.reset_password_key
	return {
	"status": 0,
	"message_text": "Mail is not verified"
	}

#resend verification OTP
@frappe.whitelist(allow_guest=True)
def resend_mail(email: str):
	user = frappe.get_doc("User", email)
	user.flags.ignore_permissions = True
	#generate 6 digit key
	number_code = random.randint(100000,999999)
	#store key in reset_password_key
	user.reset_password_key = number_code
	#store time of generation in last_reset_password_key_generated_on
	current_datetime = now_datetime()
	user.last_reset_password_key_generated_on = current_datetime
	user.save()
	frappe.db.commit()
	send_email(email,number_code)

	return {
	"status": 1,
    "message_text": "Generated a new code."
  }

#custom functions for reset pass as guest
@frappe.whitelist(allow_guest=True)
def send_otp_code(email):
	#use the above resend_mail
	pass

@frappe.whitelist(allow_guest=True)
def verify_otp_code(email, number_code, purpose="general"):
	"""
	Verify OTP and optionally generate a single-use token for password reset.

	Args:
		email: User's email
		number_code: OTP code to verify
		purpose: "general" for signup/other uses, "password_reset" to generate reset token
	"""
	user = frappe.get_doc("User", email)
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
			# If this is for password reset, generate a single-use token and store in cache
			reset_token = None
			if purpose == "password_reset":
				import secrets
				reset_token = secrets.token_urlsafe(32)
				# Store token in cache with 10 minute expiry
				cache_key = f"password_reset_token:{email}"
				frappe.cache().set_value(cache_key, reset_token, expires_in_sec=600)

			frappe.response["http_status_code"] = 200
			frappe.response["status"] = "success"
			frappe.response["message_text"] = "OTP Verified"
			if reset_token:
				frappe.response["reset_token"] = reset_token
			return
	#user.reset_password_key = number_code
	#user.last_name = "nys"

	#key = user.reset_password_key
	frappe.response["http_status_code"] = 400
	frappe.response["status"] = "error"
	frappe.response["message_text"] = "Wrong verification code"
	return

@frappe.whitelist(allow_guest=True)
def reset_password(email, new_password, reset_token):
    """
    Reset password using a single-use token obtained from OTP verification.
    Token is stored in cache and deleted after use.

    Args:
        email: User's email
        new_password: New password to set
        reset_token: Single-use token from verify_otp_code with purpose="password_reset"
    """
    try:
        # Validate inputs
        if not email or not new_password or not reset_token:
            frappe.response["http_status_code"] = 400
            frappe.response["status"] = "error"
            frappe.response["message_text"] = "Email, new password, and reset token are required."
            return

        # Get user document
        try:
            user = frappe.get_doc("User", email)
        except frappe.DoesNotExistError:
            frappe.response["http_status_code"] = 404
            frappe.response["status"] = "error"
            frappe.response["message_text"] = "User not found."
            return

        # Verify reset token from cache
        cache_key = f"password_reset_token:{email}"
        stored_token = frappe.cache().get_value(cache_key)

        if not stored_token:
            frappe.response["http_status_code"] = 400
            frappe.response["status"] = "error"
            frappe.response["message_text"] = "Invalid or expired reset token. Please request a new OTP."
            return

        # Check token match
        if stored_token != reset_token:
            frappe.response["http_status_code"] = 400
            frappe.response["status"] = "error"
            frappe.response["message_text"] = "Invalid reset token."
            return

        # Update password and delete token from cache (single-use)
        user.new_password = new_password
        user.save(ignore_permissions=True)
        frappe.db.commit()

        # Delete the token to ensure single-use
        frappe.cache().delete_value(cache_key)

        frappe.response["http_status_code"] = 200
        frappe.response["status"] = "success"
        frappe.response["message_text"] = "Password reset successful."

    except frappe.PermissionError:
        frappe.response["http_status_code"] = 403
        frappe.response["status"] = "error"
        frappe.response["message_text"] = "You do not have permission to reset the password."

    except Exception as e:
        frappe.log_error(message=str(e), title="Password Reset Error")
        frappe.response["http_status_code"] = 500
        frappe.response["status"] = "error"
        frappe.response["message_text"] = "An unexpected error occurred."



@frappe.whitelist(allow_guest = True)
def app_login(usr,pwd):
	login_manager = LoginManager()
	login_manager.authenticate(usr,pwd)
	login_manager.post_login()
	if frappe.response['message'] == 'Logged In':
		user = login_manager.user
		frappe.response['key_details'] = generate_key(user)
		frappe.response['user_details'] = get_user_details(user)
		frappe.response['profile_form'] = get_profile_form(user)
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
	user_details = frappe.get_all("User",filters={"name":user},fields=["name","first_name","last_name"])
	if user_details:
		user_roles = frappe.get_roles(user)
		user_details[0]["user_roles"] = user_roles
		return user_details
	
def get_profile_form(user):
	#usersignup means user applied with details, appuser means approved users.
	if frappe.db.exists("UserSignups", user):
		if frappe.db.exists("AppUser", user):
			ifi_id = frappe.db.get_value("AppUser", {"name": user},"ifi_id")
			return{
				"details": True,
				"approved": True,
				"ifi_id": ifi_id
			}
		else:
			return{
				"details": True,
				"approved": False
			}
	else:
		return{
				"details": False,
				"approved": False
			}