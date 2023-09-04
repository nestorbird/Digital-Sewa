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

    setup(frm) {
		frm.set_query('license_plate', () => {
			return {
				filters: {
					customer : frm.doc.customer
				}
			}
		})
	},

    refresh: function (frm) {
        console.log("refresh");
        $('.btn-comment').on('click', function () {
            frappe.call({
                    method: 'digital_sewa.digital_sewa.doctype.ds_ticket.ds_ticket.pause_unpause_client',
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
                        method: 'digital_sewa.hook.dialaer_api.dial_call',
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
        if (frm.doc.__unsaved) {
            frm.set_df_property("create_lead", "hidden", 1);
        }
    },
    after_save(frm) {
        frm.set_df_property("create_lead", "hidden", 0);
        refresh_field("create_lead")
    },
    create_lead(frm) {
        var lead_doc = frappe.model.get_new_doc("Lead");

        // Set the value of the "test_crm" field in the new Lead document
        lead_doc.from_ticket = frm.doc.name;

        // Open the Lead form for data entry
        frappe.set_route("Form", "Lead", lead_doc.name);
    },

    before_save: function (frm) {
        frm.doc.is_new_ticket = 0;
    },
	onload: function (frm) {
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
	},

    customer : frm => {
		frappe.db.get_value("Customer", frm.doc.customer, ['customer_primary_address'], (address) => {
            // console.log(address.message)
            frappe.db.get_doc("Address", address.customer_primary_address).then( r => {
                frm.set_value('state', r.state);
                frm.set_value('pincode', r.pincode);
                frm.set_value('customer_address', r.address_line1 + r.address_line2);
                frm.set_value('city', r.city);
                frm.set_value('region', r.country);
                frm.set_value('email_id', r.email_id);
                frm.save()
            })
        })
    }
});
