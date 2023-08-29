import frappe
import  requests
from digital_seva.dialer_integration.dialer_call_api import make_agent_log

@frappe.whitelist(allow_guest=True)
def contact_number(doctype, txt, searchfield, start, page_len, filters):
    data = frappe.db.sql("""select ds.mobile_number from `tabDS Ticket` ds.customer_name=%s""",)
    return data

@frappe.whitelist(allow_guest=True)
def dial_call(mobile_number):
    agent_number=frappe.db.get_value("Agent",frappe.session.user,'agent_number')
    base_url = "https://api.servetel.in/v1/click_to_call" if frappe.db.get_single_value("Dialer Settings",'integration')=="Servetel" else ""


    body={
    "agent_number": agent_number,
    "caller_id": frappe.db.get_single_value("Dialer Settings",'caller_id'),
    "destination_number":mobile_number if "+91" in mobile_number else "+91"+ mobile_number
    }
    headers={
        "Content-Type":"application/json",
        "Authorization":frappe.db.get_single_value("Dialer Settings",'authorization')
    }    
    print(base_url,"URL")
    response = requests.post(base_url, headers=headers,json=body)
    data = response.json()
    print("data",data)
    if data['success']:
        log_data={
                "mobile_number":body['destination_number'] ,
                "user":frappe.session.user,
                "call_id":frappe.db.get_single_value("Dialer Settings",'caller_id')
        }
        make_agent_log(log_data)
        frappe.db.set_value("Agent",frappe.session.user,{"status":"Busy","break_log":""}) 
    return data
