from odoo import models, fields

class Teacher(models.Model):
    _name = "institution.teacher"

    name = fields.Char(string="Name", required=True)
    subject = fields.Char(string="Subject Specialization")
    phone = fields.Char(string="Phone")

    course_ids = fields.Many2many(
        'institution.course',
        string="Courses"
    )