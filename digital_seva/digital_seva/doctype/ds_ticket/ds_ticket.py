# Copyright (c) 2023, NestorBird and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
from frappe.utils import  now
from digital_seva.dialer_integration.dialer_call_api import update_status

class DSTicket(Document):
    def validate(doc, method=None):
        if doc.is_new():
            lead = frappe.new_doc("Lead")
            lead.update({
                "organization_lead": doc.organization_lead,  
                "company_name": doc.company_name,
                "email_id": doc.email_id,
                "lead_owner": doc.lead_owner,
                "status": doc.status,
                "salutation": doc.salutation,
                "designation": doc.designation,
                "gender": doc.gender,
                "source": doc.source,
                "customer": doc.customer,
                "campaign_name": doc.campaign_name,
                "image": doc.image,
                "contact_by": doc.contact_by,
                "contact_date": doc.contact_date,
                "ends_on": doc.ends_on,
                "notes": doc.notes,
                "address_type": doc.address_type,
                "address_title": doc.address_title,
                "address_line1":doc.address_line_1,
                "city": doc.city,
                "county": doc.county,
                "state": doc.state,
                "country": doc.country,
                "phone": doc.phone,
                "mobile_no": doc.mobile_no,
                "fax": doc.fax,
                "website": doc.website,
                "type": doc.type,
                "market_segment": doc.market_segment,
                "industry": doc.industry,
                "request_type": doc.request_type,
                "company": doc.company,
                "territory": doc.territory,
                "language": doc.language,
                "unsubscribed": doc.unsubscribed,
                "blog_subscriber": doc.blog_subscriber,
                "title": doc.title
            })
            if doc.email_id:
                email_parts = doc.email_id.split("@")
                if len(email_parts) > 1:
                    lead.lead_name = email_parts[0]
                else:
                    lead.lead_name = doc.email_id

            lead.insert(ignore_mandatory=True)
    


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

