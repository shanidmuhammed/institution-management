{
    'name': 'Advance Payment Settlement',
    'version': '1.0',
    'summary': 'Advance Payment Settlement',
    'description': "",
    'author': 'Shanid V v',
    'license': 'LGPL-3',
    'application': True,
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/advance_sequence.xml',
        'wizard/advance_settlement_wizard_views.xml',
        'views/advance_payment_views.xml',
        'views/account_move_views.xml',
        'views/res_company_views.xml',
        'views/advance_menu.xml'
    ]
}