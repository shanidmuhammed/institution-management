from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Batch(models.Model):
    _name = 'institution.batch'

    course_id=fields.Many2one(
        'institution.course',
        string='Course',
        required=True
    )
    name = fields.Char(string="Batch Name", required=True)
    code = fields.Char(string="Batch Code", required=True)
    start_date = fields.Date(string="Batch Start Date", required=True)
    end_date = fields.Date(string="Batch End Date")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], string="Status", default='draft', required=True)

    student_ids = fields.One2many('institution.student', 'batch_id', string="Students")

    @api.constrains('start_date', 'end_date')
    def _check_end_date(self):
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError("The End Date cannot be earlier than the Start Date!")

    @api.model
    def _check_batch_expiry(self):
        """ This function is called by the Cron Job to auto-complete batches """
        today = fields.Date.today()

        # 1. Search for batches that are NOT completed but have expired
        # We check for 'draft' or 'in_progress' states
        expired_batches = self.search([
            ('state', '!=', 'completed'),
            ('end_date', '<', today)
        ])

        # 2. Update them all at once (Bulk Write for performance)
        if expired_batches:
            expired_batches.write({'state': 'completed'})

            # Optional: Log a note in the chatter
            # for batch in expired_batches:
            #     batch.message_post(body="System: Batch automatically marked as Completed due to expiry.")
