from odoo import models, fields

class Teacher(models.Model):
    _name = "institution.teacher"
    _description = "Teacher"

    name = fields.Char(string="Name", required=True)
    subject = fields.Char(string="Subject Specialization")
    phone = fields.Char(string="Phone")

    user_id = fields.Many2one('res.users', string="Related User")

    course_ids = fields.Many2many(
        'institution.course',
        string="Courses"
    )