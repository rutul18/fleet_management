from datetime import datetime
from odoo import api, fields, models
from odoo.tools import ustr



class AccountMoveLine(models.Model):
    """Account Move Line Model."""

    _inherit = "account.move.line"

    fleet_rent_id = fields.Many2one('vehicle.rental',
                                    string='Rental Vehicle')




class AccountInvoice(models.Model):
    """Account Invoice Model."""

    _inherit = "account.invoice"

    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle',
                                 help='Vehicle Name.')
    fleet_rent_id = fields.Many2one('fleet.rent',
                                    string='Rental Vehicle')
    is_deposit_inv = fields.Boolean(string="Is Deposit Invoice")
    is_deposit_return_inv = fields.Boolean(string="Is Deposit Return Invoice")


class AccountPayment(models.Model):
    """Account Payment Model."""

    _inherit = 'account.payment'

    fleet_rent_id = fields.Many2one('fleet.rent',
                                    string='Rental Vehicle',
                                    help='Rental Vehicle Name')

    def _create_payment_entry(self, amount):

        res = super(AccountPayment, self)._create_payment_entry(amount)
        res.line_ids.write({
            'fleet_rent_id': self.fleet_rent_id and self.fleet_rent_id.id or False,
            })
        return res

    @api.multi
    def post(self):
        """Overridden Method to update tenancy infromation."""
        inv_obj = self.env['account.invoice']
        rent_sched_obj = self.env['tenancy.rent.schedule']
        if self._context.get('active_ids', False):
            for invoice in inv_obj.browse(self._context['active_ids']):
                if invoice.fleet_rent_id:
                    self.write({
                        'fleet_rent_id': invoice.fleet_rent_id and
                        invoice.fleet_rent_id.id or False
                    })
        res = super(AccountPayment, self).post()
        user = self.env.user
        notes = 'Your Rent Payment is Registered by' + " " + user.name + \
            " " + 'on' + " " + ustr(datetime.now().date())
        for invoice in self.invoice_ids:
            for rent_line in rent_sched_obj.search([
                    ('invc_id', '=', invoice and invoice.id or False)]):
                tenancy_vals = {'pen_amt': 0.0}
                if rent_line.invc_id:
                    tenancy_vals.update({
                        'pen_amt': rent_line.invc_id.residual or 0.0
                    })
                    if rent_line.invc_id.state == 'paid':
                        tenancy_vals.update({
                            'paid': True,
                            'move_check': True,
                            'state': 'paid',
                            'note': notes,
                        })
                rent_line.write(tenancy_vals)
            if self._context.get('active_model', False) and \
                    self._context['active_model'] == 'account.invoice':
                for inv in inv_obj.browse(self._context['active_ids']):
                    if inv.fleet_rent_id and inv.is_deposit_return_inv:
                        inv.fleet_rent_id.write({
                            'is_deposit_return': True,
                            'amount_return': inv.amount_total - inv.residual or 0.0
                        })
        return res