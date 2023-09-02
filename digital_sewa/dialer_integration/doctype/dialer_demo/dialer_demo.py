# Copyright (c) 2023, NestorBird Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
import requests
from frappe.model.document import Document

class DialerDemo(Document):
	pass



@frappe.whitelist(allow_guest=True)
def dial_demo_call(mobile_number,agent_number,sr_number,caller_id):
    base_url = frappe.db.get_single_value("Knowlarity Settings",'base_url')


    body={
    "k_number": "+91"+ sr_number,
    "agent_number": "+91"+ agent_number,
    "customer_number": "+91"+ mobile_number,
    "caller_id": "+91" + caller_id
    }
    
    response = requests.post(base_url, headers={
        "Content-Type":"application/json",
        "Authorization":frappe.db.get_single_value("Knowlarity Settings",'authorization'),
        "x-api-key":frappe.db.get_single_value("Knowlarity Settings",'x_api_key')
    },json=body)
    data = response.json()
    return data