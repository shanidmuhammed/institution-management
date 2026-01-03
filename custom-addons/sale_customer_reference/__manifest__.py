{
    'name': 'Sale Customer Reference',
    'author': 'Shanid V V',
    'depends': ['base', 'sale', 'account'],
    'application': True,
    'summary': 'Sale Customer Reference',
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order.xml',
        'views/account_invoice.xml',
        'views/stock_picking.xml',
        'report/sale_report_action.xml',
        'report/sale_report_template.xml',
        'views/menu.xml'
    ],
    'license': 'LGPL-3'
}