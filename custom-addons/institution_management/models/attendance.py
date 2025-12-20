from odoo import models, fields, api

class InstitutionAttendance(models.Model):
    _name = 'institution.attendance'
    _description = 'Daily Attendance Sheet'
    _rec_name = 'date'

    batch_id = fields.Many2one('institution.batch', string="Batch", required=True)
    date = fields.Date(string="Date", default=fields.Date.context_today, required=True)

    line_ids = fields.One2many('institution.attendance.line', 'attendance_id', string="Students")

    @api.onchange('batch_id')
    def _onchange_batch_id(self):
        students = self.env['institution.student'].search([('batch_id', '=', self.batch_id.id)])

        lines = []
        for student in students:
            lines.append((0, 0, {
                'student_id': student.id,
                'is_present': True  # Default to Present
            }))

        self.line_ids = [(5, 0, 0)] + lines


class InstitutionAttendanceLine(models.Model):
    _name = 'institution.attendance.line'
    _description = 'Attendance Line'

    attendance_id = fields.Many2one('institution.attendance', string="Attendance Sheet")

    student_id = fields.Many2one('institution.student', string="Student")
    is_present = fields.Boolean(string="Present", default=True)

    batch_id = fields.Many2one('institution.batch', related='attendance_id.batch_id', store=True, string="Batch")
    date = fields.Date(related='attendance_id.date', store=True, string="Date")
