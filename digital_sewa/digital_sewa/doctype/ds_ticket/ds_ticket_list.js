frappe.listview_settings['DS Ticket'] = {
    refresh: function(frm) {
        $('.custom-btn-group').hide();
        $(".comment-count").hide();
        $(".frappe-timestamp").hide();
        $(".avatar-small").hide();
        frm.page.sidebar.remove(); // this removes the sidebar
        frm.page.wrapper.find(".layout-main-section-wrapper").removeClass("col-md-10"); // this removes class "col-md-10" from content block, which sets width to 83%
    },

    onload:function(listview) {
        $('.navbar .navbar-brand').css('pointer-events','none')
        $(".level-item:contains('Name')").text("Ticket Number")
        // listview.page.actions.find('[data-label="Edit"],[data-label="Assign To"],[data-label="Print"],[data-label="Delete"],[data-label="Add Tags"],[data-label="Apply Assignment Rule"]').parent().parent().remove()
}
}
