// Copyright (c) 2023, NestorBird Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Dialer Settings', {
	integration: function(frm) {
		frm.set_value("base_url","")
		frm.set_value("authorization","")
	}
});
