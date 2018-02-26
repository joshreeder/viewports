import frappe
def get_context(context):
    #context.data = frappe.db.sql("select * from `tabUser`")
    #print "context",context.data
    context.data = "test data"