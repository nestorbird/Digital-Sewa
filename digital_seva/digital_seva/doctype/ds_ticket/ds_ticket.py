# Copyright (c) 2023, NestorBird and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
from frappe.utils import  now
from digital_seva.dialer_integration.dialer_call_api import update_status

class DSTicket(Document):
	pass



@frappe.whitelist()
def pause_unpause_client(state, type):
    print("Type", "State",type,state)
    status="Available"
    break_log=""
    if type not in ["Unpause","resolve"]:
        new_breaklog=frappe.new_doc("Break Log")
        new_breaklog.start_time=now()
        new_breaklog.break_type=type
        new_breaklog.agent=frappe.session.user
        new_breaklog.save(ignore_permissions=1)
        status="Busy"
        break_log=new_breaklog.name
    else:
        last_break=frappe.db.get_value('Agent',frappe.session.user,'break_log')
        if last_break:
            frappe.db.set_value("Break Log",last_break,"end_time",now())       
    return update_status(status,break_log)


@frappe.whitelist()
def update_unique_no(mobile_no, unique_no):
    frappe.db.sql("""UPDATE `tabDS Ticket` SET unique_no='{unique_no}' , is_new_ticket=1
    where mobile_number='{mobile_no}'""".format(unique_no=unique_no, mobile_no=mobile_no))	



@frappe.whitelist()
def break_links():
    if frappe.db.exists("Agent",frappe.session.user):
        agent=frappe.get_doc("Agent",frappe.session.user)
        if agent.status !="Available":
            if not agent.break_log:
                return True
            else:
                return []
    return frappe.db.get_list('Break Type',{'is_active': 1},['name'])              
	# 	if agent.status !="Available":
	# 		return []
	# return frappe.db.get_list('Break Type',{'is_active': 1},['name'])			

