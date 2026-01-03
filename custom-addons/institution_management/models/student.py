from odoo import models, fields, api
from datetime import date

class Student(models.Model):
    _name = "institution.student"
    _description = "Student"

    name = fields.Char(string='Name', required= True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', required=True)
    dob = fields.Date(string="Date of Birth", required=True)
    guardian_name = fields.Char(string="Guardian Name", required=True)
    contact_number = fields.Char(string="Contact Number", required=True)
    place = fields.Char(string="Place", required=True)

    batch_id = fields.Many2one('institution.batch', string='Batch')

    course_id = fields.Many2one('institution.course',  related='batch_id.course_id' , string='Course')

    user_id = fields.Many2one('res.users', string='User')

    is_registered = fields.Boolean(string="Registered", default=False, readonly=True)

    # fee_status = fields.Selection(
    #     related='fee_id.state',
    #     string='Fee Status',
    #     readonly=True,
    #     store=True
    # )
    ref = fields.Char(string="Student ID", readonly=True, default='New')

    age=fields.Integer(string="Age", compute='_compute_age')
    @api.depends('dob')
    def _compute_age(self):
        for record in self:
            if record.dob:
                record.age = date.today().year - record.dob.year
            else:
                record.age = 0


    @api.model
    def create(self, vals):
        for vals in vals:
            if vals.get('ref', 'New') == 'New':
                vals['ref'] = self.env['ir.sequence'].next_by_code('institution.student') or 'New'

        return super(Student, self).create(vals)

    def action_open_register_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Register Student',
            'res_model': 'student.register.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_student_id': self.id
            }
        }