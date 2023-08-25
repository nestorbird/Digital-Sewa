function codeAddress() {
    this.homebutton = $(".dropdown-message").replaceWith(``)
    $("#toolbar-user").append(`<a class="dropdown-item" href="/app/user">           Users
              </a>`)
    var break_link = ""
    frappe.call({
        method:'digital_seva.digital_seva.doctype.ds_ticket.ds_ticket.break_links',
        args:{}
    }).then((res) => {
        console.log("res",res.message)
        for (var data in res.message) {
            console.log(data)

            break_link += `<a class="dropdown-item" onclick="
                     frappe.call({
                            method: 'digital_seva.digital_seva.doctype.ds_ticket.ds_ticket.pause_unpause_client',
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
        const params = window.location.origin
        this.reportbutton = $(`
        <div class="dropdown">
  <button style="padding: 7px; margin: 6px;" class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
    MIS Reports
  </button>
  <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
    <a id = "login_report" class="dropdown-item" href="/app/query-report/Login Logout Report">Login Logout Report</a>
    <a id = "agent_productive" class="dropdown-item" href="/app/query-report/Agent Productivity";>Agent Productivity</a>
    <a id = "raw_dump" class="dropdown-item" href="/app/query-report/Raw Dump">Raw Dump</a>
    <a id = "ticket_sla" class="dropdown-item" href="/app/query-report/Ticket SLA">Ticket SLA</a>
    <a id = "ticket_report" class="dropdown-item" href="/app/query-report/Ticket Summary Report">Ticket Summary Report</a>
  </div>
</div>
        
        `).insertAfter($('.dropdown-help'))
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

    //     $(".dropdown-help").replaceWith(`
    //     <li  name="subject" style="padding: 2px; margin: 6px;" class="btn">        
    //     <select " class="form-control" id="select1" onchange="getData(this.value)">
    //     // <option class="a" value="A">Available</option>
    //     // <option class="c" value="C">Busy</option>
    //     </select>  
    //      </li>
      
        
    //   `);
    $(".dropdown-help").replaceWith(`
    <li class="nav-item dropdown dropdown-help dropdown-mobile d-none d-lg-block">
    <button class="btn btn-default icon-btn" style="padding: 5px">
          <a class="nav-link" data-toggle="dropdown" href="#" onclick="return false;">Break
          <span>
                  <svg class="icon icon-xs"><use href="#icon-small-down"> </use> </svg>
          </span>
          </a>
          <div class="dropdown-menu dropdown-menu-right" id="toolbar-help" role="menu">
          <div id="help-links"></div>
                 <div class="dropdown-divider documentation-links" style="display: none;"></div> 
                 ${break_link}
                 <a class="dropdown-item"  onclick="
                 frappe.call({
                        method: 'digital_seva.digital_seva.doctype.ds_ticket.ds_ticket.pause_unpause_client',
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
                 
                 ">          Unpause Incoming Call          </a>
          </div>
          </button>
    </li>
  `);
//   window.location.reload()

    //   $(".form-control").change(function(){
    //     var $option = $(this).find('option:selected');
    //     var text = $option.text()
    //     frappe.call({
    //         method: 'digital_seva.dialer_integration.dialer_call_api.update_status',
    //         args: {
    //                 'type': text
    //             },
    //         callback: (res) => {
    //             let fail=JSON.stringify(res.message['message'])
    //             let pass=JSON.stringify(res.message['status'])
    //             console.log(fail,pass);
    //             if (fail){
    //                 frappe.db.set_value("Agent",frappe.session.user,"status",text)
    //             frappe.msgprint('<p><b><i>' + fail  + '</p></b></i>');
    
    //         }
        
    //         else{

    //             if (pass.replace(/^"(.+(?="$))"$/, '$1')=="Available"){
        
    //          frappe.msgprint('<p><b><i>Status has been changed , Now Agent is Available</p></b></i>');
    //             }
    //             else{
    //                 frappe.msgprint('<p><b><i>Status has been changed , Now Agent is Busy</p></b></i>');
    //             }

    //         }
        
    //     }
    //  });
    //   });

    });
}

window.onload = codeAddress;
$(document).ready(function () {
        // frappe.db.exists("Agent",frappe.session.user).then(r=>{
        //     if (r===True){
        //     frappe.call({
        //         method: 'digital_seva.dialer_integration.dialer_call_api.update_status',
        //         args: {
        //                 'type': 'Available'
        //             }
        //          });
        //         }
        //      })
    
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
                            method: "digital_seva.digital_seva.doctype.ds_ticket.ds_ticket.update_unique_no",
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
                        method: "digital_seva.digital_seva.doctype.ds_ticket.ds_ticket.update_unique_no",
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

            document.getElementById("select1").selectedIndex = 1; 

            frappe.call({
                method: 'digital_seva.dialer_integration.dialer_call_api.update_status',
                args: {
                        'type': 'Busy'
                    }

    });
});


    frappe.realtime.on('call_disconnected', (data) => {


        console.log(data,"call_disconnected")

        document.getElementById("select1").selectedIndex = 0; 
        
        frappe.call({
            method: 'digital_seva.dialer_integration.dialer_call_api.update_status',
            args: {
                    'type': 'Available'
                }

});

    });

    document.getElementsByClassName("navbar-brand ")[0].onclick = function () {
        document.getElementsByClassName("navbar-brand ")[0].href = "/app/ds-ticket";
    };
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
