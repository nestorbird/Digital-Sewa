import frappe


def success_response(http_status_code=200, data={}, message="Success"):
    frappe.response["data"] = {
        "http_status_code": http_status_code,
        "message": message,
        "response": data
    }


def failed_response(http_status_code=400, response={}, message="Invalid request"):
    frappe.response["data"] = {
        "http_status_code": http_status_code,
        "message": message,
        "response": response
    }
