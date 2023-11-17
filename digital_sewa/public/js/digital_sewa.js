function codeAddress() {
    this.homebutton = $(".dropdown-message").replaceWith(``)
    $("#toolbar-user").append(`<a class="dropdown-item" href="/app/user">           Users
              </a>`)
    var break_link = ""
    frappe.call({
        method:'digital_sewa.digital_sewa.doctype.ds_ticket.ds_ticket.break_links',
        args:{}
    }).then((res) => {
        console.log("res",typeof(res.message))
        if (res.message==true){
            $(".dropdown-help").replaceWith(`
            <a class="nav-link" style="margin: auto; box-shadow: inset 0 1px 1px rgba(0, 0, 0, .075), 0 0 8px rgb(37, 150, 190);" data-toggle="dropdown" href="#" onclick="return false;">On Call
            `)

        }
        else if (res.message.length>0){
        for (var data in res.message) {
            console.log(data)

            break_link += `<a class="dropdown-item" onclick="
                     frappe.call({
                            method: 'digital_sewa.digital_sewa.doctype.ds_ticket.ds_ticket.pause_unpause_client',
                            args: {
                                    'state': 'pause',
                                    'type': '${res.message[data].name}'
                                },
                            callback: (res) => {
                                console.log('<',res);
                                frappe.msgprint({
                                    title: __('Notification'),
                                    indicator: 'green',
                                    message: 'The Break ' + '${res.message[data].name}' + ' has started'
                                });
                                window.location.reload()

                            }
                     });
                     
                     ">           ${res.message[data].name}          </a>`
        }
        $(".dropdown-help").replaceWith(`
        <li class="nav-item dropdown dropdown-help dropdown-mobile d-none d-lg-block">
        <button class="btn btn-default icon-btn" style="padding: 5px">
      <a class="nav-link" data-toggle="dropdown" href="#" onclick="return false;">Take Break
      <span>
              <svg class="icon icon-xs"><use href="#icon-small-down"> </use> </svg>
      </span>
      </a>
      <div class="dropdown-menu dropdown-menu-right" id="toolbar-help" role="menu">
      <div id="help-links"></div>
             <div class="dropdown-divider documentation-links" style="display: none;"></div> 
             ${break_link}
      </div>
      </button>
      </li>
      `);
      }
      else{
        $(".dropdown-help").replaceWith(`
        <a class="nav-link" style="margin: auto; box-shadow: inset 0 1px 1px rgba(0, 0, 0, .075), 0 0 8px rgb(37, 150, 190);" data-toggle="dropdown" href="#" onclick="
         frappe.call({
                method: 'digital_sewa.digital_sewa.doctype.ds_ticket.ds_ticket.pause_unpause_client',
                args: {
                        'state': 'unpause',
                        'type': 'Unpause'
                    },
                callback: (res) => {
                    frappe.msgprint({
                        title: __('Notification'),
                        indicator: 'green',
                        message: 'The Break has Ended'
                    });
                    window.location.reload()
                }
         });
         ;">End Break
         `);
        

      } 
        
        const params = window.location.origin
        $('#login_report').click(function () {
            window.location = params + "/app/query-report/" + "Login Logout Report";
        });
        $('#agent_productive').click(function () {
            window.location = params + "/app/query-report/" + "Agent Productivity";
        });
        $('#raw_dump').click(function () {
            window.location = params + "/app/query-report/" + "Raw Dump";
        });
        $('#ticket_sla').click(function () {
            window.location = params + "/app/query-report/" + "Ticket SLA";
        });
        $('#ticket_report').click(function () {
            window.location = params + "/app/query-report/" + "Ticket Summary Report";
        });

    });
}

window.onload = codeAddress;
$(document).ready(function () {
    let route = frappe.get_route()
    if ((route[0]==="Workspaces" || route[0]==="") && (frappe.user.has_role("Digital Sewa Agent"))){
        setTimeout(()=>{
            frappe.call({
                method: "digital_sewa.dialer_integration.dialer_call_api.workspace_to_ds",
                args: {
                        unique_no: 11111,
                        mobile_number: "+919876543210",
                        user:frappe.session.user
                },
                callback: function (r) {
                    console.log("testing", r)
                    frappe.msgprint(r.message.message);
                    if (r.message.url === "Already Exist") {
                        frappe.set_route("List", "DS Ticket", { mobile_number: r.message.mobile_number });
                    } else {
                        frappe.set_route("Form", "DS Ticket", r.message.ds_ticket);
                    }
                }
            });
        },10000)
    }
    
    // hide search bar
    // document.getElementsByClassName('search-bar')[0].style.visibility = 'hidden';
    // frappe.realtime.on('msgprint', (data) => {
    //     console.log("**********")
    //     console.log(JSON.stringify(data));
    //     console.log("**********")
    //     var test = JSON.stringify(data)
    //     frappe.msgprint('<p>' + test + '</p>')
    // });
    frappe.realtime.on('msgprint', (data) => {
        console.log(data,"--------------call_connected")

        if (data["url"] == "Already Exist") {
            var docu = frappe.new_doc("DS Ticket");
            frappe.set_route("Form", "DS Ticket", docu.name);
            frappe.set_route("List", "DS Ticket", {
                ticket_status: "Open",
                mobile_number: data["mobile_number"]
            }).then((e) => {
                let next_button = document.querySelectorAll(".list-row-col.ellipsis.list-subject.level");
                for (var i = 1; i < next_button.length; i++) {
                    next_button[i].onclick = function () {
                        frappe.call({
                            method: "digital_sewa.digital_sewa.doctype.ds_ticket.ds_ticket.update_unique_no",
                            args: {
                                mobile_no: data["mobile_number"],
                                unique_no: data.unique_no
                            },
                            callback: function (r) {
                                console.log("mkm", r);
                            }
                        });
                    }
                }
            });
            let nbutton = document.querySelectorAll(".list-row-col.ellipsis.list-subject.level");
            for (var i = 1; i < nbutton.length; i++) {
                nbutton[i].onclick = function () {
                    frappe.call({
                        method: "digital_sewa.digital_sewa.doctype.ds_ticket.ds_ticket.update_unique_no",
                        args: {
                            mobile_no: data["mobile_number"],
                            unique_no: data.unique_no
                        },
                        callback: function (r) {
                            console.log("mkm", r);
                        }
                    });
                }
            }

        } else {
            window.location.replace(data["url"]);
            document.getElementById("select1").selectedIndex = 1; 
        }
    });

    frappe.realtime.on('call_connected', (data) => {

            console.log(data,"--------------call_connected")

            // document.getElementById("select1").selectedIndex = 1; 

            frappe.call({
                method: 'digital_sewa.dialer_integration.dialer_call_api.update_status',
                args: {
                        'type': 'Busy'
                    }

    });
    window.location.reload()
});


    frappe.realtime.on('call_disconnected', (data) => {


        console.log(data,"call_disconnected")

        // document.getElementById("select1").selectedIndex = 0; 
        
        frappe.call({
            method: 'digital_sewa.dialer_integration.dialer_call_api.update_status',
            args: {
                    'type': 'Available'
                }

});
    window.location.reload()
    });


    // document.getElementsByClassName("navbar-brand ")[0].onclick = function () {
    //     document.getElementsByClassName("navbar-brand ")[0].href = "/app/ds-ticket";
    // };
    // setInterval(my_alert_func, 4000); // Set to 3 seconds
    // function my_alert_func() {
    //     frappe.db.get_value("User", {"name": frappe.session.user}, "availability_status", (r) => {
    //         if (r["availability_status"]) {
    //             document.getElementsByClassName("dropdown-notifications")[0].innerHTML = `
    //                     <div id="availability_status" style="     font-weight: 900;
    //             margin-top: -50px;
    //             color: black;
    //             margin-left: 58px;">${r["availability_status"]}</div>`
    //         }
    //     });
    // }
});
