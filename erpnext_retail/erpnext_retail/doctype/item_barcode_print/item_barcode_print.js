// Copyright (c) 2019, Techlift and contributors
// For license information, please see license.txt

frappe.ui.form.on('Item Barcode Print', {
	// refresh: function(frm) {

	// }
	before_submit: function(frm) {
		frappe.call({
			method: "erpnext_retail.erpnext_retail.doctype.item_barcode_print.item_barcode_print.download_csv_on_submit",
			args: {"doc":frm.doc, "name":frm.doc.name},
			callback: function(r) {console.log('r',r.message,'r');
			window.open(r.message, "_blank");
		}
	})
	},
});

frappe.ui.form.on("Barcode Print Items", "item", function(frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	if (d.item){
		frappe.call({
			method: 'frappe.client.get_value',
			args: {
				'doctype': 'Item Price Details',
				'fieldname': ["rate"],
				'parent': 'Item'
			},
			async: false,
			callback: function(r) {
				if(r.message.rate){
					d.rate = r.message.rate
	                refresh_field("rate", d.name, d.parentfield);
				}
			}
		});
	}
	
});
