from odoo import models, fields

class StudentRegisterWizard(models.TransientModel):
    _name = 'student.register.wizard'
    _description = 'Student Registration Wizard'

    student_id = fields.Many2one('institution.student', string="Student", required=True)

    def action_confirm(self):
        self.student_id.is_registered = True
