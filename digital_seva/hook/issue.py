import frappe

def after_insert(doc,method):
    if doc.dialler_support:
        dialler_support = frappe.get_doc("Dialer Support", doc.dialler_support)
        dialler_support.add_comment("Comment", """
                            <div>
                                <h5>New Ticket has been Created</h5>
                                <p>Ticket has been created with Ticket ID {ticket_id}. <a href="{link}">Click Here</a> to open</p>
                            </div>
                        """.format(ticket_id=doc.name,
                                   link = '/app/issue/{issue_name}'.format(issue_name = doc.name)))

