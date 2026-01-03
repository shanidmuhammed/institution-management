{
    'name': 'Institution Management',
    'version': '1.0',
    'author': 'Shanid V V',
    'application': True,
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/student_sequence.xml',
        'views/course_view.xml',
        'views/teacher_view.xml',
        'views/category_view.xml',
        'views/fee_view.xml',
        'views/attendance_view.xml',
        'views/student_view.xml',
        'views/student_register_wizard_view.xml',
        'views/menu.xml'
    ],
    'license': 'LGPL-3'
}