// Copyright (c) 2023, NestorBird and contributors
// For license information, please see license.txt

function randString(x) {
    var s = "";
    var today = new Date();
    var date = String(today.getFullYear()).substring(2, 4) + '' + (today.getMonth() + 1);
    var time = today.getHours() + "" + today.getMinutes();
    var dateTime = date + time;
    while (s.length < x && x > 0) {
        var r = Math.random();
        s += (r < 0.1 ? Math.floor(r * 100) : String.fromCharCode(Math.floor(r * 26) + (r > 0.5 ? 97 : 65)));
    }
    return s.toUpperCase() + dateTime;
}

frappe.ui.form.on('DS Ticket', {
    refresh: function (frm) {
        console.log("refresh");
        $('.btn-comment').on('click', function () {
            frappe.call({
                    method: 'digital_seva.digital_seva.doctype.ds_ticket.ds_ticket.pause_unpause_client',
                    args: {
                        'state': 'unpause',
                        'type': 'resolve'
                    },
                    callback: (res) => {
                        console.log("resolve", res)
                    }
                });
        });
		$(".page-icon-group").hide();

		frm.add_custom_button(__('&#128222;'), function () {

            if (frm.doc.mobile_number){
                    frappe.call({
                        method: 'digital_seva.hook.dialaer_api.dial_call',
                        args: {
                            mobile_number: frm.doc.mobile_number
                        },
                        callback(r) {
                            console.log(r.message,"-------")
                            if (r.message['success']) {
                                console.log("abd",r.message)
                                

                                frappe.msgprint(__('Connecting to Call'));
                            }

                            else{

                                frappe.msgprint(__('Connection Failed, Please check the parameters'));

                            }
                        },
                    })}

                else{
                    frappe.throw("Please Enter the Customer Number")
                }
        })
	},
    before_save: function (frm) {
        frm.doc.is_new_ticket = 0;
    },
	onload: function (frm) {
        $('.btn.btn-primary.btn-sm').hide();
        if (!frm.doc.__unsaved) {
            document.getElementsByClassName('form-reviews')[0].style.display = "none";

            document.getElementsByClassName('form-shared')[0].style.display = "none";
            document.getElementsByClassName('form-sidebar-stats')[0].style.display = "none";
            document.getElementsByClassName('modified-by')[0].style.display = "none";
            document.getElementsByClassName('created-by')[0].style.display = "none";
        }
        if (!frm.doc.unique_no) {
            frm.set_value("unique_no", randString(16));
        }
       if (!frm.custom_button_added) {
            frm.add_custom_button('Create Lead', function () {
                frm.save().then(() => {
                    frappe.new_doc("Lead", {
                        ds_name: frm.doc.name,
                        source: "Cold Calling"
                    });
                });
            });
            frm.custom_button_added = true;
        }
        var customerField = "mobile_number";
        if (frm.fields_dict[customerField]) {
            frm.fields_dict[customerField].$wrapper.after(frm.custom_buttons['Create Lead']);
        }
    },
});












