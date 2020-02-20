from odoo import fields, models


class ResPartner(models.Model):
    """Res Partner Model."""

    _inherit = "res.partner"

    is_driver = fields.Boolean(string="Is Driver")
    is_tenant = fields.Boolean(string="Is Tenant")
    tenant = fields.Boolean(string="Is Tenant?")
    tenancy_ids = fields.One2many('vehicle.rental', 'tenant_id', string='Rental Detail', help='Rental Details')
    maintanance_ids = fields.One2many('maintenance.cost', 'tenant_id', string='Maintenance Details')
    doc_name = fields.Char(string='Filename')
    id_attachment = fields.Binary(string='Identity Proof')




class ResUsers(models.Model):
    """Res Users Model."""

    _inherit = "res.users"

    fleet_rent_ids = fields.One2many('vehicle.rental', 'tenant_id', string='Rental Details',
                                     help='Rental Details')
    maintanance_ids = fields.One2many('maintenance.cost', 'tenant_id', string='Maintenance Details')
