from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, Warning
from odoo import fields, models, api
from odoo.tools import ustr, DEFAULT_SERVER_DATE_FORMAT as DF, \
    DEFAULT_SERVER_DATETIME_FORMAT as DTF


class VehicleRental(models.Model):
    """Fleet Vehicle Rental."""
    _name = "vehicle.rental"
    _description = "Vehicle Rental Details"

    @api.multi
    def Set_Conform(self):
        """Button Conform."""
        for vehicle in self:
            vehicle.state = 'open'


    @api.multi
    def Set_Deposit_Receive(self):
        """Button Deposit Receive."""
        print("\n:::Set_Deposit_Receive:::", Set_Deposit_Receive)

    @api.multi
    def Set_To_Draft(self):
        """Button Set TO Draft."""
        # print("\n:::Set_To_Draft:::", Set_To_Draft)
        for rent in self:
            rent.state = 'draft'

    @api.multi
    def Set_Close(self):
        """Button Set To Close"""
        print("\n:::Set_Close:::", Set_Close)

    @api.multi
    def Set_Done(self):
        """Button Set Done."""
        # print("\n:::Set_Done:::", Set_Done)
        for rent in self:
            if not rent.rent_schedule_ids:
                raise Warning("Without Rent schedule .\
                 you can not done the rent. .\
                 please first create the rent schedule")
            rent.state = 'done'


    @api.multi
    def create_rent_schedule(self):
        """Button Create Rent Schedule."""

        for rent in self:
            for rent_line in rent.rent_schedule_ids:
                print("\n:::rent_line:::", rent_line)

            rent_obj = self.env['tenancy.rent.schedule']
            currency = rent.currency_id or False
            vehicle = rent.vehicle_id or False
            tenent = rent.tenant_id or False
            if rent.st_date and rent.rent_id \
                    and rent.rent_id.rent_type:
                interval = int(rent.rent_id.duration)
                date_st = rent.st_date
                if rent.rent_id.rent_type == 'month':
                    for i in range(0, interval):
                        date_st = date_st + relativedelta(months=int(1))
                        print("\n:::i:::", i)
                        rent_obj.create({
                            'start_date': date_st.strftime(DTF),
                            'amount': rent.vehicle_rent or False,
                            'vehicle_id': vehicle and vehicle.id or False,
                            'fleet_rent_ids': rent.id,
                            'currency_id': currency and currency.id or False,
                            'rel_tenant_id': tenent and tenent.id or False,
                        })
            rent.cr_rent_btn = True
        return True


    @api.model
    def create(self, vals):
        """Sequence create Method"""

        seq = self.env['ir.sequence'].next_by_code('vehicle.rental')

        if vals and not vals.get('name', False):
            vals.update({'name': seq})
        student = super(VehicleRental, self).create(vals)
        return student


    @api.multi
    @api.depends('rent_id', 'st_date')
    def _create_date(self):
        for rent in self:
            if rent.rent_id and rent.st_date:
                if rent.rent_id.rent_type == 'month':
                    rent.end_date = rent.st_date + \
                        relativedelta(months=int(rent.rent_id.duration))

    @api.depends('maintanance_ids', 'maintanance_ids.cost')
    def _total_maintenance_cost(self):
        """Method to calculate total maintenance."""
        for rent in self:
            total_amt = 0
            for cost_line in rent.maintanance_ids:
                total_amt += cost_line.cost or 0.0
            rent.maintanance_cost = total_amt \


    @api.multi
    def action_rent_done(self):
        """Method to Change rent state to done."""
        rent_sched_obj = self.env['tenancy.rent.schedule']
        for rent in self:
            if not rent.rent_schedule_ids:
                raise ValidationError("Without Rent schedule you can not done the rent.\
                    please first create the rent schedule.")
            if rent.rent_schedule_ids:
                rent_schedule = rent_sched_obj.search([
                    ('paid', '=', False),
                    ('id', 'in', rent.rent_schedule_ids.ids)])
                if rent_schedule:
                    raise ValidationError("Scheduled Rents is remaining.\
                            please first pay scheduled rents.!!")
                rent.state = 'done'

    @api.multi
    def count_invoice(self):
        """Method to count Out Invoice."""
        obj = self.env['account.invoice']
        for rent in self:
            rent.invoice_count = obj.search_count([
                ('type', '=', 'out_invoice'),
                ('fleet_rent_id', '=', rent.id),
                ('is_deposit_inv', '=', True)])

    @api.multi
    def count_refund_invoice(self):
        """Method to count Refund Invoice."""
        obj = self.env['account.invoice']
        for rent in self:
            rent.refund_inv_count = obj.search_count([
                ('type', '=', 'out_refund'),
                ('fleet_rent_id', '=', rent.id),
                ('is_deposit_return_inv', '=', True)])



    name = fields.Char(string="Name", translate=True, copy=False, default="New")
    state = fields.Selection([('draft', 'New'), ('open', 'In Progress'),
                              ('pending', 'To Renew'), ('close', 'Closed'),
                              ('done', 'Done'),
                              ('cancelled', 'Cancelled')],
                             string='Status', default='draft', copy=False)
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle")
    tenant_id = fields.Many2one('res.users', string="Tenant")
    company_id = fields.Many2one('res.company', string="Company")
    currency_id = fields.Many2one('res.currency', string="Currency")
    vehicle_rent = fields.Float(string='Vehicle Rent',  currency_field='currency_id')
    contract_date = fields.Datetime(string='Contract Date', default=lambda *a: datetime.now())
    deposit_amount = fields.Float(string="Deposit Amount", currency_field='currency_id')
    contract_id = fields.Many2one('res.partner', string="Contract")
    st_date = fields.Datetime(string="Start Date",  default=lambda *a: datetime.now())
    end_date = fields.Datetime(string="Expire Date", compute="_create_date" )
    description = fields.Text(string="description")
    rent_schedule_ids = fields.One2many('tenancy.rent.schedule', 'fleet_rent_ids', string="Rental")
    maintanance_ids = fields.One2many('maintenance.cost', 'fleet_rent_id', string="Maintenance Cost")
    maint_type = fields.Many2one('maintenance.type', string="Maintenance Type")
    date = fields.Date(string="Date")
    label = fields.Char(string="label")
    reference = fields.Char(string="Reference")
    account_move_line_ids = fields.One2many('account.move.line', 'fleet_rent_id', string='Entries')
    move_id = fields.Many2one('account.move', string="Journal Entry")
    journal_id = fields.Many2one('account.journal', string="Journal")
    account_id = fields.Many2one('account.account', string="Account")
    debit_id = fields.Char(string="Debit")
    credit_id = fields.Char(string="Credit")
    close_reson = fields.Char(string="Close Reason")
    description = fields.Char(string="Description")
    rent_id = fields.Many2one('rent.type', string="Rent Type")
    deposit_received = fields.Boolean(string="Deposit Received?")
    deposit_returned = fields.Boolean(string="Deposit Returned?")
    total_rent = fields.Monetary(string="Total Rent")
    invoice_count = fields.Integer(compute='count_invoice', string="Invoice Count")
    refund_inv_count = fields.Integer(compute='count_refund_invoice', string="Refund")
    maintanance_cost = fields.Float(string="Maintanance Cost", compute='_total_maintenance_cost', store=True,
                                    help="Add Maintenance Cost.")
    currency_id = fields.Many2one('res.currency',
                                  default=lambda self: self.env['res.company']._get_user_currency(),
                                  string='Currency',
                                  help="The optional other currency \ "
                                       "if it is a multi-currency entry.")
    odometer = fields.Float(string="Last Odometer")
    rent_close_by = fields.Many2one('res.users', string="Rent Close By", copy=False)
    date_close = fields.Datetime(string="Rent Close Date", copy=False)
    cr_rent_btn = fields.Boolean(string='Hide Rent Button', copy=False)



class MaintenanceType(models.Model):
    """Maintenace Type Model."""

    _name = 'maintenance.type'
    _description = 'Vehicle Maintenance Type'

    name = fields.Char(string='Maintenance Type', size=50, required=True)
    cost = fields.Float(string='Maintenance Cost', help='insert the cost')


class MaintenanaceCost(models.Model):
    """Maintenace Cost Model."""

    _name = 'maintenance.cost'
    _description = 'Vehicle Maintenance Cost'

    maint_type = fields.Many2one('maintenance.type', string='Maintenance Type')
    cost = fields.Float(string='Maintenance Cost', help='insert the cost')
    fleet_rent_id = fields.Many2one('vehicle.rental', string='Rental Vehicle', help='Rental Vehicle Name.')
    tenant_id = fields.Many2one('res.users')


class TenancyRentSchedule(models.Model):
    """Tenancy Rent Schedule."""

    _name = "tenancy.rent.schedule"
    _description = 'Tenancy Rent Schedule'


    note = fields.Text(string='Notes', help='Additional Notes.')
    currency_id = fields.Many2one('res.currency', string='Currency')
    amount = fields.Float(string='Amount', defualt='0.0', help="Rent Amount.")
    start_date = fields.Datetime(string='Date', help='Start Date.', default=lambda *a: datetime.now())
    end_date = fields.Date(string='End Date', help='End Date.')
    cheque_detail = fields.Char(string='Cheque Detail', size=30)
    move_id = fields.Many2one('account.move', string='Depreciation Entry')
    move_check = fields.Boolean(compute='_get_move_check', string='Posted', store=True)
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle', help='Vehicle Name.')
    fleet_rent_ids = fields.Many2one('vehicle.rental', string='Rental Vehicle', help='Rental Vehicle Name.')
    pen_amt = fields.Float(string='Pending Amount', help='Pending Amount.')
    paid = fields.Boolean(string="Paid")
    post = fields.Boolean(string="Post")
    rel_tenant_id = fields.Many2one('res.partner', string="Tenant")
    state = fields.Selection([('draft', 'Draft'), ('open', 'Open'),
                              ('paid', 'Paid'), ('cancel', 'Cancel')], string="State", default="draft")
    invc_id = fields.Many2one('account.invoice', string='Invoice')
    inv = fields.Boolean(string='Is Invoice?')
    pen_amt = fields.Float(string='Pending Amount', help='Pending Amount.')


    @api.depends('move_id')
    def _get_move_check(self):
        for rent_sched in self:
            rent_sched.move_check = bool(rent_sched.move_id)

    @api.multi
    def create_invoice(self):
        """Create invoice for Rent Schedule."""
        self.ensure_one()
        journal_id = self.env['account.journal'].search([
            ('type', '=', 'sale')], limit=1)
        rent = self.fleet_rent_ids or False
        vehicle = rent and rent.vehicle_id or False
        if vehicle and not vehicle.income_acc_id:
            raise Warning('Please Configure Income Account from Vehicle !!')
        inv_line_main = {
            'origin': 'tenancy.rent.schedule',
            'name': 'Maintenance Cost',
            'price_unit': rent and rent.maintanance_cost or 0.0,
            'quantity': 1,
            'account_id': rent and rent.vehicle_id and rent.vehicle_id.income_acc_id and
                          rent.vehicle_id.income_acc_id.id or False,
        }

        inv_line_values = {
            'origin': 'tenancy.rent.schedule',
            'name': 'Tenancy(Rent) Cost',
            'price_unit': self.amount or 0.0,
            'quantity': 1,
            'account_id': vehicle and vehicle.income_acc_id.id or False,
        }

        inv_values = {
            'partner_id': rent and rent.tenant_id and
            rent.tenant_id.partner_id and
            rent.tenant_id.partner_id.id or False,
            'type': 'out_invoice',
            'vehicle_id': vehicle and vehicle.id or False,
            'date_invoice': datetime.now().strftime(DF),
            'journal_id': journal_id and journal_id.id or False,
            'account_id': rent and rent.tenant_id and
            rent.tenant_id.property_account_receivable_id and
            rent.tenant_id.property_account_receivable_id.id or False,
            'fleet_rent_ids': rent and rent.id or False,
        }
        if self.fleet_rent_ids and self.fleet_rent_ids.maintanance_cost:
            inv_values.update({'invoice_line_ids': [(0, 0, inv_line_values),
                                                    (0, 0, inv_line_main)]})
        else:
            inv_values.update(
                {'invoice_line_ids': [(0, 0, inv_line_values)]})
        acc_id = self.env['account.invoice'].create(inv_values)
        self.write({'invc_id': acc_id.id, 'inv': True})
        context = dict(self._context or {})
        wiz_form_id = self.env['ir.model.data'].get_object_reference(
            'account', 'invoice_form')[1]

        return {
            'view_type': 'form',
            'view_id': wiz_form_id,
            'view_mode': 'form',
            'res_model': 'account.invoice',
            'res_id': self.invc_id.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': context,
        }

    @api.multi
    def open_invoice(self):
        """Method Open Invoice."""
        context = dict(self._context or {})
        wiz_form_id = self.env['ir.model.data'].get_object_reference(
            'account', 'invoice_form')[1]

        return {
            'view_type': 'form',
            'view_id': wiz_form_id,
            'view_mode': 'form',
            'res_model': 'account.invoice',
            'res_id': self.invc_id.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': context,
        }


class RentType(models.Model):
    _name = "rent.type"
    _description = "Rent Type"

    name = fields.Char(string="Name")
    duration = fields.Integer(string="Duration", required=True, default='1')
    rent_type = fields.Selection([('hour', 'Hour'), ('day', 'Day'),
                                 ('week', 'Week'), ('month', 'Months'),
                                 ('year', 'Year')],
                                 default='month', string="Rent Type", required=True)






