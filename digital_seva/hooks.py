from . import __version__ as app_version

app_name = "digital_seva"
app_title = "Digital Seva"
app_publisher = "NestorBird"
app_description = "This app provides extended ticketing solution on ERPNext or any other App build on Frappe."
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@nestorbird.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/digital_seva/css/digital_seva.css"
app_include_js = "/assets/digital_seva/js/digital_seva.js"

# include js, css files in header of web template
# web_include_css = "/assets/digital_seva/css/digital_seva.css"
# web_include_js = "/assets/digital_seva/js/digital_seva.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "digital_seva/public/scss/website"

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
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "digital_seva.install.before_install"
# after_install = "digital_seva.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "digital_seva.uninstall.before_uninstall"
# after_uninstall = "digital_seva.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "digital_seva.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

fixtures = [
     {
        "dt": "Custom Field", "filters":
        [
            [
                "name", "in", [
						"DS Ticket-title",
                        "DS Ticket-blog_subscriber",
                        "DS Ticket-unsubscribed",
                        "DS Ticket-language",
                        "DS Ticket-territory",
                        "DS Ticket-company",
                        "DS Ticket-column_break_534al",
                        "DS Ticket-request_type",
                        "DS Ticket-industry",
                        "DS Ticket-market_segment",
                        "DS Ticket-type",
                        "DS Ticket-more_info",
                        "DS Ticket-website",
                        "DS Ticket-fax",
                        "DS Ticket-mobile_no",
                        "DS Ticket-phone",
                        "DS Ticket-contact_section",
                        "DS Ticket-country",
                        "DS Ticket-contact_html",
                        "DS Ticket-column_break_wey1j",
                        "DS Ticket-county",
                        "DS Ticket-address_line_2",
                        "DS Ticket-address_line_1",
                        "DS Ticket-address_title",
                        "DS Ticket-address_type",
                        "DS Ticket-address_html",
                        "DS Ticket-address_info",
                        "DS Ticket-notes",
                        "DS Ticket-notes_section_",
                        "DS Ticket-ends_on",
                        "DS Ticket-contact_date",
                        "DS Ticket-column_break_h3xl4",
                        "DS Ticket-contact_by",
                        "DS Ticket-section_break_rvgvx",
                        "DS Ticket-image",
                        "DS Ticket-campaign_name",
                        "DS Ticket-source",
                        "DS Ticket-gender",
                        "DS Ticket-designation",
                        "DS Ticket-salutation",
                        "DS Ticket-status",
                        "DS Ticket-lead_owner",
                        "DS Ticket-column_break_zlxhn",
                        "DS Ticket-company_name",
                        "DS Ticket-lead_name",
                        "DS Ticket-lead_details",
                        "DS Ticket-organization_lead",
                        "DS Ticket-section_break_qiahl"
                ]]  
        ]},

]







# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"digital_seva.tasks.all"
#	],
#	"daily": [
#		"digital_seva.tasks.daily"
#	],
#	"hourly": [
#		"digital_seva.tasks.hourly"
#	],
#	"weekly": [
#		"digital_seva.tasks.weekly"
#	]
#	"monthly": [
#		"digital_seva.tasks.monthly"
#	]
# }

# Testing
# -------

# before_tests = "digital_seva.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "digital_seva.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "digital_seva.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Request Events
# ----------------
# before_request = ["digital_seva.utils.before_request"]
# after_request = ["digital_seva.utils.after_request"]

# Job Events
# ----------
# before_job = ["digital_seva.utils.before_job"]
# after_job = ["digital_seva.utils.after_job"]

# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"digital_seva.auth.validate"
# ]

default_mail_footer = """
	<span>
		
	</span>
"""