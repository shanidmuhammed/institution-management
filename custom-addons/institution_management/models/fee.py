from odoo import models, fields

class Fee(models.Model):
    _name = 'institution.fee'
    _description = 'Student Fee'
    _rec_name = 'student_id'

    student_id = fields.Many2one('institution.student', string='Student', required=True)
    amount = fields.Float(string='Paid Amount', required=True)
    date = fields.Date(string='Fee Date', required=True)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('paid', 'Paid')
    ])

    total_fee = fields.Float(related='student_id.course_id.fee', string='Total Fee', store=True, readonly=True)
