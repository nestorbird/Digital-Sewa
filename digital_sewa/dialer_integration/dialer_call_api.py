import frappe
import requests
import json
import string
import random
from digital_sewa.utils import success_response, failed_response


@frappe.whitelist(allow_guest=True)
def data_feed():
    return None
    while True:
        try:
            url='https://konnect.knowlarity.com:8100/update-stream/62c312a2-cb01-4a40-a630-125cfd5f79ba/konnect'
            r = requests.get(url,stream=True,timeout=43200)
            stop_feed=frappe.db.get_single_value("Knowlarity Settings",'feed')
            if  stop_feed == 0:
                    r.close()
                    frappe.throw("Command received to stop")
            if r.status_code == 200:
                frappe.db.set_value("Knowlarity Settings","Knowlarity Settings",'call',1)
                print("success +++++++")
                for line in r.iter_lines():
                    if line and (line.decode())[6:]:
                        keys=json.loads((line.decode())[6:])
                        if keys.get('agent_number'):
                            print(keys)
                            user=frappe.get_doc("User",{"agent_number":(keys.get('agent_number'))[3:]})
                            if keys.get('agent_number') and keys.get('call_solution')=="inbound" and keys.get("event_type")=="ORIGINATE":
                                print("incoming call--------")
                                unique_no=''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
                                call_json = {
                                            "unique_no": str(unique_no),
                                            "mobile_number": str(keys.get('customer_number')),
                                            "extension_no": "1106",
                                            "queue_no": "8171",
                                            "user":user.name
                                            }
                                create_dialer_support(call_json)

                            if keys.get('agent_number') and (keys.get('call_solution')=="inbound" or keys.get('business_call_type')=="Outbound") and (keys.get("event_type")=="ANSWER" or  keys.get("event_type")=="AGENT_ANSWER") :
                                print("incoming call answered")
                                frappe.publish_realtime( "call_connected", message="Busy", user=user.name )

                            if keys.get('agent_number') and (keys.get('call_solution')=="inbound" or keys.get('business_call_type')=="Outbound" or keys.get('business_call_type')=="Unanswered") and keys.get("event_type")=="HANGUP" and keys.get('leg_identifier')== 'customer':
                                    print("call disconnected")
                                    frappe.publish_realtime( "call_disconnected", message="Available", user=user.name )

            else:
                frappe.db.set_value("Knowlarity Settings","Knowlarity Settings",'call',0)
       
  
        # except Exception as e:
        #     frappe.db.set_value("Knowlarity Settings","Knowlarity Settings",'call',0)
        #     frappe.log_error("{0}".format(e))

        except requests.exceptions.Timeout:
            frappe.db.set_value("Knowlarity Settings","Knowlarity Settings",'call',0)
            frappe.log_error("Request timed out")
        except requests.exceptions.RequestException as e:
            frappe.db.set_value("Knowlarity Settings","Knowlarity Settings",'call',0)
            frappe.log_error("Error: " + str(e))


@frappe.whitelist(allow_guest=True)
def update_status(type,break_log=None):
    status="unblock" if type=="Available" else "block"
    agent_id=frappe.db.get_value("Agent",frappe.session.user,"agent_id")
    url= f"https://api.servetel.in/v1/agent/{agent_id}/{status}"
    headers = {
        "Authorization":frappe.db.get_single_value("Dialer Settings",'authorization')
        }
    response = requests.post(url, headers=headers)

    data = response.json()
    print(data)
    frappe.db.set_value("Agent",frappe.session.user,{"status":type,"break_log":break_log if break_log else ""})
    return data


@frappe.whitelist(allow_guest=True)
def dial_on_agent():
    data=frappe.safe_decode(frappe.local.request.get_data())
    keys=frappe.parse_json(data)
    agent_id=list(filter(lambda x : x["type"]=="Agent" and x['num']==keys['agent_number'],keys['call_flow']))
    if keys["agent_number"]:
        agent=frappe.get_doc("Agent",{"agent_id":list(agent_id)[0]['id']})
        call_json = {
                "unique_no": keys['uuid'],
                "mobile_number": keys['customer_no_with_prefix '],
                "user":agent.name,
                "call_id":keys['call_id']
                }
        create_dialer_support(call_json) 


@frappe.whitelist()
def create_dialer_support(data):
    if not data.get("unique_no"):
        return failed_response(message="Please Provide Unique Number")
    if not data.get("mobile_number"):
        return failed_response(message="Please Provide Mobile Number")
    filter = {"mobile_number": data.get("mobile_number")}
    if (len(frappe.get_all("DS Ticket", filters=filter)) > 0):
        datas = {"url": "Already Exist", "mobile_number": data.get("mobile_number"),
                "unique_no": data.get("unique_no"),
                "message": "Tickets found against this customer number."}
        
    else:
        new_dialer_support = frappe.new_doc("DS Ticket")
        new_dialer_support.unique_no = data.get("unique_no")
        new_dialer_support.mobile_number = data.get("mobile_number")
        new_dialer_support.is_new_ticket = 1
        new_dialer_support.save(ignore_permissions=True)
        frappe.db.commit()

        url = str(frappe.utils.get_url()) + "/app/ds-ticket/" + new_dialer_support.name
        datas = {"url": url,
                "unique_no": new_dialer_support.unique_no, "message": "Redirecting to Incoming Call..."}
    make_agent_log(data)            
    frappe.publish_realtime(
        "msgprint", message=datas, user=data.get('user')
    )


@frappe.whitelist(allow_guest=True)
def hang_up():
    data = frappe.safe_decode(frappe.local.request.get_data())
    data=frappe.parse_json(data)
    if data["call_connected"] and data["call_id"]:
        ds_ticket=frappe.db.get_value("DS Ticket",{"mobile_number":data["customer_no_with_prefix "] if "+" in data["customer_no_with_prefix "] else "+"+data["customer_no_with_prefix "]},"name") 
        if data["direction"]=="inbound":    
            if frappe.db.exists("Agent Log",{"call_id":data["call_id"]}):
                agent_log=frappe.get_doc("Agent Log",{"call_id":data["call_id"]})
                agent_log.start_time=data["start_stamp"]
                agent_log.answer_time=data["answer_stamp"]
                agent_log.end_time=data["end_stamp"]
                agent_log.dialer_duration=data["duration"]
                agent_log.hold_duration=data["agent_ring_time"]
                agent_log.no_of_hold=data["outbound_sec"]
                agent_log.ds_ticket=ds_ticket
                agent_log.log_completions=1
                agent_log.save(ignore_permissions=True)
        elif data["direction"]=="clicktocall":
            if frappe.db.exists("Agent Log",{"ds_ticket":ds_ticket,"log_completions":0}):
                agent_log=frappe.get_doc("Agent Log",{"ds_ticket":ds_ticket,"log_completions":0})
                agent_log.start_time=data["start_stamp"]
                agent_log.answer_time=data["answer_stamp"]
                agent_log.end_time=data["end_stamp"]
                agent_log.dialer_duration=data["duration"]
                agent_log.hold_duration=data["agent_ring_time"]
                agent_log.no_of_hold=data["outbound_sec"]
                agent_log.ds_ticket=ds_ticket
                agent_log.log_completions=1
                agent_log.save(ignore_permissions=True)                  
        agent=frappe.get_doc("Agent",{"agent_id":data["answered_agent"]["id"]})
        frappe.db.set_value("Agent",agent.name,{"status":"Available","break_log": ""})
        # frappe.publish_realtime( "call_disconnected", message="Available", user=agent.name )


def make_agent_log(data):
    agent_log=frappe.new_doc("Agent Log")
    agent_log.start_time=frappe.utils.now()
    agent_log.call_id=data.get("call_id")
    agent_log.agent=data.get("user")
    agent_log.ds_ticket=frappe.db.get_value("DS Ticket",{"mobile_number":data.get("mobile_number")},"name")
    agent_log.save(ignore_permissions=True)


@frappe.whitelist(allow_guest=True)
def answer_by_agent():
    data=frappe.safe_decode(frappe.local.request.get_data())
    keys=frappe.parse_json(data)
    if frappe.db.exists("Agent",{"agent_number":keys["answer_agent_number"]}):
        agent=frappe.get_doc("Agent",{"agent_number":keys["answer_agent_number"]})
        frappe.db.set_value("Agent",agent.name,{"status":"Busy","break_log": ""})
        # frappe.publish_realtime( "call_connected", message="Busy", user=agent.name )

@frappe.whitelist(allow_guest=True)
def trigger():
    if frappe.local.request.get_data():
        data = frappe.parse_json(frappe.safe_decode(frappe.local.request.get_data()))
    if frappe.form_dict:
        data = frappe.form_dict
    if frappe.local.request.args:
        data = frappe.local.request.args
    doc = frappe.new_doc("Webhook Testing")
    doc.body = data
    doc.save()
    return



@frappe.whitelist()
def workspace_to_ds(unique_no,mobile_number,user):
    if not unique_no:
        return failed_response(message="Please Provide Unique Number")
    if not mobile_number:
        return failed_response(message="Please Provide Mobile Number")
    filter = {"mobile_number": mobile_number}
    if (len(frappe.get_all("DS Ticket", filters=filter)) > 0):
        datas = {"url": "Already Exist", "mobile_number": mobile_number,
                "unique_no": unique_no,
                "message": f"Redirecting to Incoming Call, {mobile_number}"}
            
    else:
        new_dialer_support = frappe.new_doc("DS Ticket")
        new_dialer_support.unique_no = unique_no
        new_dialer_support.mobile_number = mobile_number
        new_dialer_support.is_new_ticket = 1
        new_dialer_support.save(ignore_permissions=True)
        frappe.db.commit()
        url = str(frappe.utils.get_url()) + "/app/ds-ticket/" + new_dialer_support.name
        datas = {"url": url,"ds_ticket":new_dialer_support.name,
                "unique_no": new_dialer_support.unique_no, "message": f"Redirecting to Incoming Call, {new_dialer_support.mobile_number}"}
        frappe.publish_realtime("custom_call_sound", user='user')
    return datas



@frappe.whitelist()
def save_incoming_call(mobile_number, csrf_token):
    existing_entry = frappe.get_all(
        "Incoming Call Demo",
        filters={
            "csrf_token": csrf_token
        },
        fields=["name"]
    )

    if not existing_entry:
        incoming_call = frappe.get_doc({
            "doctype": "Incoming Call Demo",
            "mobile_number": mobile_number,
            "csrf_token": csrf_token
        })

        incoming_call.insert(ignore_permissions=True)
        return "New Incoming Call saved successfully"
    else:
        return "CSRF token already exists in Incoming Call"


