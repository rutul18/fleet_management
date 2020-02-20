from odoo import models, fields, api
from datetime import datetime, date
from odoo.tools import ustr


class WizardCloseReason(models.TransientModel):
    _name = 'close.reason'
    _description = "Wizard Close Reason"

    reason = fields.Char(string="Reason")

    @api.multi
    def close_reason(self):
        user = self.env.user
        date = datetime.now().date()
        notes ='Your Rent Payment is Cancelled by' + " " + user.name + \
                  " " + 'on' + " " + ustr(date)
        if self._context.get('active_id', False) and \
                self._context.get('active_model', False):
            for rent in self.env[self._context['active_model']].browse(
                    self._context.get('active_id', False)):
                tenancy_obj = self.env['tenancy.rent.schedule'].search(([('state', 'in', ['draft', 'open']),
                                                                       ('fleet_rent_id', '=', rent.id)]))
                tenancy_obj.write({'state': 'cancel',
                                   'note': 'notes'})
                rent.write({'state': 'close',
                            'close_reson': self.reason,
                            'date_close': date.today(),
                            'rent_close_by': self._uid})
                return True

