// Copyright (c) 2023, NestorBird Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Dialer Demo', {
	call: function(frm) {

	if (frm.doc.call_made_from=="Agent"){
		frappe.call({
			method: 'fasttag_erp.dialer_integration.doctype.dialer_demo.dialer_demo.dial_demo_call',
			args: {
				mobile_number: frm.doc.customer_number,
				sr_number:frm.doc.sr_no,
				agent_number:frm.doc.agent_number,
				caller_id:frm.doc.caller_id
			},
			callback(r) {
				if (r.message['success']) {
					

					frappe.msgprint(__('Connecting to Call'));
				}

				else{

					frappe.msgprint(__('Connection Failed, Please check the parameters'));

				}
			},
		})
	}

	}
});
