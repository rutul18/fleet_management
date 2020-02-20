from odoo import fields, models


class FleetExtent(models.Model):
    """Fleet Extend Fields"""


    _inherit = 'fleet.vehicle'
    _description = "Fleet Extends Details"

    income_acc_id = fields.Many2one('account.account', string="Income Account")
    expence_acc_id = fields.Many2one("account.account", string="Expense Account")


