import frappe
import  requests

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
    "caller_id": "08069858830",
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
    return data
