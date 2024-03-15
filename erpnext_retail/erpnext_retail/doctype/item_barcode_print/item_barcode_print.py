# -*- coding: utf-8 -*-
# Copyright (c) 2019, Techlift and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
import requests
import urllib.request  
import csv
import io
import webbrowser
from frappe.model.document import Document
from frappe.utils.file_manager import get_file
from frappe.utils.file_manager import download_file

class ItemBarcodePrint(Document):
    # def after_insert(self):
         
    def on_submit(self):
        self.generate_csv_on_submit()
    #       download_csv_on_submit(self)




    def generate_csv_on_submit(self):
        # Check if the document has a child table
        if self.get("items"):
            # Fetch data from the child table
            data = frappe.get_all("Barcode Print Items", {'parent': self.name}, ['item','number_of_print', 'item_name','article','size','rate','custom_was','custom_discount','company'])
            print(f"data {data}")
            # Create CSV string
            csv_string = ",".join(data[0].keys()) + "\n"
            for row in data:
                csv_string += ",".join(str(row[field]) for field in data[0].keys()) + "\n"
            print(f"csv_string {csv_string}")
            # Create a file
            csv_file = io.StringIO()
            csv_file.write(csv_string)
            url = f"rp.luckybee.in/files/{self.name}_items_data.csv"

            # Attach the CSV file to the parent document
            file_doc = frappe.get_doc({
                'doctype': 'File',
                'file_name': f'{self.name}_items_data.csv',
                'attached_to_doctype': self.doctype,
                'attached_to_name': self.name,
                'content': csv_file.getvalue(),
                'is_private': 0  # Optional: Set to 1 to make the file private
            })

            file_doc.save(ignore_permissions=True)
            file_name = frappe.get_site_path("files", f'{self.name}_items_data.csv')
            # requests.get(url)
            # file_data = get_file(file_name)
            # download_file(file_data.file_url)

@frappe.whitelist()
def download_csv_on_submit(doc,name):
     doc= json.loads(doc)
     if doc.get("items"):
        return f"https://erp.luckybee.in/files/{name}_items_data.csv"
        # url = f"https://erp.luckybee.in/files/{self.name}_items_data.csv"
        # webbrowser.open("https://google.com")
        # frappe.log_error(f'url,{webbrowser.open("https://google.com")}')
