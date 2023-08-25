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
def create_dialer_support(data,):
    pass
    # try:    
    if not data.get("unique_no"):
        return failed_response(message="Please Provide Unique Number")
    if not data.get("mobile_number"):
        return failed_response(message="Please Provide Mobile Number")
    filter = {"mobile_number": data.get("mobile_number"),
              "ticket_status": "Open"}
    if (len(frappe.get_all("DS Ticket", filters=filter)) > 0):
        datas = {"url": "Already Exist", "mobile_number": data.get("mobile_number"),
                "unique_no": data.get("unique_no"),
                "message": "Tickets found against this customer number."}
        
    else:
        new_dialer_support = frappe.new_doc("DS Ticket")
        new_dialer_support.unique_no = data.get("unique_no")
        new_dialer_support.mobile_number = data.get("mobile_number")
        # new_dialer_support.extension_no = data.get("extension_no")
        # new_dialer_support.queue_no = data.get("queue_no")
        new_dialer_support.is_new_ticket = 1
        new_dialer_support.save(ignore_permissions=True)
        frappe.db.commit()

        url = str(frappe.utils.get_url()) + "/app/ds-ticket/" + new_dialer_support.name
        datas = {"url": url,
                "unique_no": new_dialer_support.unique_no, "message": "Redirecting to Incoming Call..."}
        
    print(data.get('user'),datas)
    frappe.publish_realtime(
        "msgprint", message=datas, user=data.get('user')
    )
    # return success_response(data=data)
    # except Exception as e:
    #     return failed_response(message="Exception Occurred" + str(e))


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
    # if type != 'resolve':
    #     if user.availability_status == "Pause" and state == 'pause':
    #         frappe.throw("User Already in Pause State")
    #     if user.availability_status == "Available" and state == 'unpause':
    #         frappe.throw("User Already in Available State")
    #     if not (state == 'unpause' and type == 'Unpause'):
    #         doc = frappe.new_doc("Break History")
    #         break_type = frappe.get_doc("Break Type", type)
    #         doc.user = frappe.session.user
    #         doc.reason = type
    #         doc.break_duration = break_type.break_duration or "00:15:00"
    #         doc.save(ignore_permissions=True)
    #         frappe.db.commit()
    #     else:
    #         last_break = frappe.get_last_doc("Break History", filters={"user": frappe.session.user})
    #         last_break.break_duration = datetime.now() - last_break.date
    #         last_break.is_available_again = 1
    #         m, s = divmod(last_break.break_duration.total_seconds(), 60)
    #         H = int(m // 60) if len(str(int(m // 60))) > 1 else '0'+str(int(m // 60))
    #         M = int(m % 60) if len(str(int(m % 60))) > 1 else '0'+str(int(m % 60))
    #         S = int(s) if len(str(int(s))) > 1 else '0'+str(int(s))
    #         H = '23' if int(H) > 23 else H
    #         M = '59' if int(M) > 59 else M
    #         S = '59' if int(S) > 59 else S
    #         last_break.break_duration = "{}:{}:{}".format(H , M , S)
    #         last_break.save()
    #         frappe.db.commit()
    # else:
    #     try:
    #         last_break = frappe.get_last_doc("Break History", filters={"user": frappe.session.user})
    #         if last_break.is_available_again == 0:
    #             return "User is on break"
    #     except:
    #         pass
    # url_start = frappe.db.get_single_value(
    #     "DS Ticket Settings", "url_dialler_response")
    # send_state = 'pause' if state == 'busy' else state
    # url = url_start + "/apis/agent.php?queue={queue_number}&agent={agent_id}&action={state}&uuid={uuid}&reason={reason}".format(
    #     queue_number=user.incoming_queue_number,
    #     agent_id=user.extension_number,
    #     state=send_state,
    #     uuid=user.email,
    #     reason=type)
    # request = requests.post(url.replace(" ", "%20"))
    # response = request.json()
    # if response['Status'] == "ERROR":
    #     error_log = frappe.new_doc("Error Log")
    #     error_log.method = "DS Ticket ERROR"
    #     error_log.error = str(response)
    #     error_log.save()
    #     frappe.throw("Unable to change the state of agent. please contact admin")
    # else:
    #     if state == "pause":
    #         frappe.db.set_value(
    #             "User", frappe.session.user, "availability_status", "Pause", update_modified=False
    #         )
    #     if state == "busy":
    #         frappe.db.set_value(
    #             "User", frappe.session.user, "availability_status", "Busy", update_modified=False
    #         )
    #     if state == "unpause":
    #         frappe.db.set_value(
    #             "User", frappe.session.user, "availability_status", "Available", update_modified=False
    #         )

    # return response



@frappe.whitelist()
def update_unique_no(mobile_no, unique_no):
    frappe.db.sql("""UPDATE `tabDS Ticket` SET unique_no='{unique_no}' , is_new_ticket=1
    where mobile_number='{mobile_no}'""".format(unique_no=unique_no, mobile_no=mobile_no))	



@frappe.whitelist()
def break_links():
	if frappe.db.exists("Agent",frappe.session.user):
		agent=frappe.get_doc("Agent",frappe.session.user)
		if agent.status !="Available":
			return []
	return frappe.db.get_list('Break Type',{'is_active': 1},['name'])
	# 	else:
	# 		[]
	# else:
	# 	return frappe.get_list("Break Type",filters[["is_active","=",1]],pluck="name")			

