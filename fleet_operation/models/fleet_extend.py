from odoo import fields, models, api
from datetime import date, datetime
from odoo.tools import misc


class VehicleRegistration(models.Model):
    _inherit = 'fleet.vehicle'
    _description = "Extend field fleet vehicle"


    @api.multi
    def update_history(self):
        """Method use update color engine,battery and tire history."""
        mod_obj = self.env['ir.model.data']
        print("::::mod_obj:::", mod_obj)
        wizard_view = ""
        res_model = ""
        view_name = ""
        cr, uid, context = self.env.args
        context = dict(context)
        if context.get('history', False):
            if context.get("history", False) == "color":
                wizard_view = "update_color_info_form_view"
                res_model = "update.color.info"
                view_name = "Update Color Info"
            elif context.get("history", False) == "engine":
                wizard_view = "update_engine_info_form_view"
                res_model = "update.engine.info"
                view_name = "Update Engine Info"
            elif context.get('history', False) == 'vin':
                wizard_view = "update_vin_info_form_view"
                res_model = "update.vin.info"
                view_name = "Update Vin Info"
            elif context.get('history', False) == 'tire':
                wizard_view = "update_tire_info_form_view"
                res_model = "update.tire.info"
                view_name = "Update Tire Info"
            elif context.get('history', False) == 'battery':
                wizard_view = "update_battery_info_form_view"
                res_model = "update.battery.info"
                view_name = "Update Battery Info"
        print("::::wizard_view::::", wizard_view)

        model_data_ids = mod_obj.search([('model', '=', 'ir.ui.view'),
                                         ('name', '=', wizard_view)])
        print("::::model_data_ids:::", model_data_ids)
        resource_id = model_data_ids.read(['res_id'])
        context.update({'vehicle_ids': self._ids})
        self.env.args = cr, uid, misc.frozendict(context)
        return {
            'name': view_name,
            'context': self._context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': res_model,
            'views': [(resource_id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'new',
        }


    name = fields.Char(string="Vehicle-ID", store=True)
    odometer_check = fields.Boolean('Odometer Change', default=True)
    fuel_qty = fields.Char(string='Fuel Quality')
    fuel_type = fields.Selection([('gasoline', 'Gasoline'),
                                  ('diesel', 'Diesel'),
                                  ('petrol', 'Petrol'),
                                  ('electric', 'Electric'),
                                  ('hybrid', 'Hybrid')], 'Fuel Type',
                                 default='diesel',
                                 help='Fuel Used by the vehicle')
    oil_name = fields.Char(string='Oil Name')
    oil_capacity = fields.Char(string='Oil Capacity')
    fleet_id = fields.Integer(string='Fleet ID', help="Take this field for data migration")
    f_brand_id = fields.Many2one('fleet.vehicle.model.brand', string='Make')
    model_no = fields.Char(string='Model No', translate=True)
    license_plate = fields.Char(string='License Plate', translate=True, size=32,
                                help='License plate number of the vehicle.(ie: plate number for a vehicle)')
    active = fields.Boolean(string='Active', default=True)
    dealer_id = fields.Many2one('res.partner', string='Dealer')
    mileage = fields.Integer(string='Mileage(K/H)')
    description = fields.Text(string='About Vehicle', translate=True)
    engine_size = fields.Char(string='Engine Size', size=16)
    cylinders = fields.Integer(string='No of Cylinders')
    front_tire_size = fields.Float(string='Front Tire Size')
    front_tire_pressure = fields.Integer(string='Front Tire Pressure')
    rear_tire_size = fields.Float(string='Rear Tire Size')
    rear_tire_pressure = fields.Integer(string='Rear Tire Pressure')
    last_service_date = fields.Date(string='Last Service', readonly=True)
    next_service_date = fields.Date(string='Next Service', readonly=True)
    last_odometer = fields.Float(string='Last Service Odometer')
    last_odometer_unit = fields.Selection([('kilometers', 'Kilometers'),
                                           ('miles', 'Miles')],
                                          string='Last Odometer Unit', help='Unit of the odometer ')
    due_odometer = fields.Float(string='Next Service Odometer', readonly=True)
    due_odometer_unit = fields.Selection([('kilometers', 'Kilometers'),
                                          ('miles', 'Miles')],
                                         string='Due Odometer Units',
                                         help='Unit of the odometer ')
    left_wiper_blade = fields.Char(string='Wiper Blade(L)', size=8)
    right_wiper_blade = fields.Char(string='Wiper Blade(R)', size=8)
    rr_wiper_blade = fields.Char(string='Wiper Blade(RR)', size=8)
    vehicle_length = fields.Integer(string='Length(mm)')
    vehicle_width = fields.Integer(string='Width(mm)')
    vehicle_height = fields.Integer(string='Height(mm)')
    fuel_capacity = fields.Float(string='Fuel Capacity(l)')
    date_sold = fields.Date(string='Date Sold')
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    transfer_date = fields.Date(string='Transfer Date')
    monthly_deprication = fields.Float(string='Deprication(Monthly)')
    resale_value = fields.Float(string='Current value')
    salvage_value = fields.Float(string='Salvage Value')
    warranty_period = fields.Date(string='Warranty Upto')
    insurance_company_id = fields.Many2one('res.partner', string='Insurance Company')
    insurance_type_id = fields.Many2one('insurance.type', string='Insurance Type')
    policy_number = fields.Char(string='Policy Number', size=32)
    payment = fields.Float(string='Payment')
    start_date_insurance = fields.Date(string='Start Date')
    end_date_insurance = fields.Date(string='End Date')
    payment_deduction = fields.Float(string='Deduction')
   # fleet_attach_ids = fields.One2many('ir.attachment', 'attachment_id',string='Fleet Attachments')
    #sale_purchase_attach_ids = fields.One2many('ir.attachment', 'attachment_id_2', string='Attachments')
    #odometer = fields.Float(compute='_get_odometer', inverse='_set_odometer',
                          #  string='Last Odometer',
                           # help='Odometer measure of the vehicle at the \
                             #      moment of this log')
    vehical_color_id = fields.Many2one('color.color', string='Vehicle Color')
    vehicle_location_id = fields.Many2one('res.country.state',
                                          string='Registration State')
    vehical_division_id = fields.Many2one('vehicle.divison', string='Division')
    driver_id = fields.Many2one('res.partner', 'Driver')
    driver_identification_no = fields.Char(string='Driver ID', size=64)
    driver_contact_no = fields.Char(string='Driver Contact Number', size=64)
    main_type = fields.Selection([('vehicle', 'Vehicle'),
                                  ('non-vehicle', 'Non-Vehicle')],
                                 default='vehicle', string='Main Type')
    vechical_type_id = fields.Many2one('vehicle.type', string='Vehicle Type')
    engine_no = fields.Char(string='Engine No', size=64)
    # multi_images = fields.One2many('multi.images', 'vehicle_template_id',
    #                               'Multi Images')
    #multi_images = fields.Many2many('ir.attachment', 'fleet_vehicle_attachment_rel', 'vehicle_id', 'attachment_id',
    #                              string='Multi Images')
    state = fields.Selection([('inspection', 'Draft'),
                              ('in_progress', 'In Service'),
                              ('contract', 'On Contract'),
                              ('rent', 'On Rent'), ('complete', 'Completed'),
                              ('released', 'Released'),
                              ('write-off', 'Write-Off')],
                             string='Vehicle State', default='inspection')
    is_id_generated = fields.Boolean(string='Is Id Generated?', default=False)
    increment_odometer = fields.Float(string='Next Increment Odometer')
    last_change_status_date = fields.Date(string='Last Status Changed Date', readonly=True)
    # pending_repair_type_ids = fields.One2many('pending.repair.type', 'vehicle_rep_type_id', string='Pending Repair Types', readonly=True)
    released_date = fields.Date(string='Released Date', readonly=True)
    tire_size = fields.Char(string='Tire Size', size=64)
    tire_srno = fields.Char(string='Tire S/N', size=64)
    tire_issuance_date = fields.Date(string='Tire Issuance Date')
    battery_size = fields.Char(string='Battery Size', size=64)
    battery_srno = fields.Char(string='Battery S/N', size=64)
    battery_issuance_date = fields.Date(string='Battery Issuance Date')
    color_history_ids = fields.One2many('color.history', 'vehicle_id', string="Color History", readonly=True)
    engine_history_ids = fields.One2many('engine.history', 'vehicle_id', string="Engine History", readonly=True)
    vin_history_ids = fields.One2many('vin.history', 'vehicle_id', string="Vin History", readonly=True)
    tire_history_ids = fields.One2many('tire.history', 'vehicle_id', string="Tire History", readonly=True)
    battery_history_ids = fields.One2many('battery.history', 'vehicle_id', string="Battrey History", readonly=True)
    is_color_set = fields.Boolean(string='Is Color Set?')
    is_engine_set = fields.Boolean(string='Is Engine Set')
    is_vin_set = fields.Boolean(string='Is Vin Set?')
    is_tire_size_set = fields.Boolean(string='Is Tire Size set?')
    is_tire_srno_set = fields.Boolean(string='Is Tire Srno set?')
    is_tire_issue_set = fields.Boolean(string='Is Tire Issue set?')
    is_battery_size_set = fields.Boolean(string='Is battery Size set?')
    is_battery_srno_set = fields.Boolean(string='Is battery Srno set?')
    is_battery_issue_set = fields.Boolean(string='Is battery Issue set?')
    last_service_by_id = fields.Many2one('res.partner', string="Last Service By")
    work_order_ids = fields.One2many('fleet.vehicle.log.services', 'vehicle_id', string='Service Order')
    reg_id = fields.Many2one('res.users', string='Registered By')
    vehicle_owner = fields.Many2one('res.users', string='Vehicle Owner')
    updated_by = fields.Many2one('res.users', string='Updated By')
    updated_date = fields.Date(string='Updated date')
    work_order_close = fields.Boolean(string='Work Order Close', default=True)
    fmp_id_editable = fields.Boolean(string='Vehicle ID Editable?')
    income_acc_id = fields.Many2one("account.account", string="Income Account")
    expence_acc_id = fields.Many2one("account.account", string="Expense Account")


class ColorHistory(models.Model):
    """Model color history."""

    _name = 'color.history'
    _description = 'Color History for Vehicle'

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle")
    previous_color_id = fields.Many2one('color.color', string="Previous Color")
    current_color_id = fields.Many2one('color.color', string="New Color")
    changed_date = fields.Date(string='Change Date')
    note = fields.Text(string='Notes', translate=True)
    workorder_id = fields.Many2one('fleet.vehicle.log.services', string='Work Order')


class ColorColor(models.Model):
    """Model Color."""

    _name = 'color.color'
    _description = 'Colors'

    code = fields.Char(string='Code', size=12)
    name = fields.Char(string='Name', size=32, required=True)


class EngineHistory(models.Model):
    """Model Engine History."""

    _name = 'engine.history'
    _description = 'Engine History for Vehicle'

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle")
    previous_engine_no = fields.Char(string='Previous Engine No')
    new_engine_no = fields.Char(string='New Engine No')
    changed_date = fields.Date(string='Change Date')
    note = fields.Text('Notes', translate=True)
    workorder_id = fields.Many2one('fleet.vehicle.log.services', string='Work Order')

    @api.multi
    def copy(self, default=None):
        """Method to copy."""
        if not default:
            default = {}
        raise Warning(_('You can\'t duplicate record!'))
        return super(EngineHistory, self).copy(default=default)


class VinHistory(models.Model):
    """Model Vin History."""

    _name = 'vin.history'
    _description = 'Vin History'

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle")
    previous_vin_no = fields.Char(string='Previous Vin No')
    new_vin_no = fields.Char(string='New Vin No')
    changed_date = fields.Date(string='Change Date')
    note = fields.Text(string='Notes')
    workorder_id = fields.Many2one('fleet.vehicle.log.services', string='Work Order')


class TireHistory(models.Model):
    """Model Tire History."""

    _name = 'tire.history'
    _description = 'Tire History for Vehicle'

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle")
    previous_tire_size = fields.Char(string='Previous Tire Size', size=124)
    new_tire_size = fields.Char(string="New Tire Size", size=124)
    previous_tire_sn = fields.Char(string='Previous Tire Serial', size=124)
    new_tire_sn = fields.Char(string="New Tire Serial", size=124)
    previous_tire_issue_date = fields.Date(
        string='Previous Tire Issuance Date')
    new_tire_issue_date = fields.Date(string='New Tire Issuance Date')
    changed_date = fields.Date(string='Change Date')
    note = fields.Text(string='Notes')
    workorder_id = fields.Many2one('fleet.vehicle.log.services', string='Work Order')


class BatteryHistory(models.Model):
    """Model Battery History."""

    _name = 'battery.history'
    _description = 'Battery History for Vehicle'

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle")
    previous_battery_size = fields.Char(string='Previous Battery Size',
                                        size=124)
    new_battery_size = fields.Char(string="New Battery Size", size=124)
    previous_battery_sn = fields.Char(string='Previous Battery Serial',
                                      size=124)
    new_battery_sn = fields.Char(string="New Battery Serial", size=124)
    previous_battery_issue_date = fields.Date(
        string='Previous Battery Issuance Date')
    new_battery_issue_date = fields.Date(string='New Battery Issuance Date')
    changed_date = fields.Date(string='Change Date')
    note = fields.Text(string='Notes')
    workorder_id = fields.Many2one('fleet.vehicle.log.services', string='Work Order')


class PendingRepairType(models.Model):
    """Model Pending Repair Type."""

    _name = 'pending.repair.type'
    _description = 'Pending Repait Type'

    vehicle_rep_type_id = fields.Many2one('fleet.vehicle', string="Vehicle")
    repair_type_id = fields.Many2one('repair.type', string="Repair Type")
    name = fields.Char(string='Work Order #')
    categ_id = fields.Many2one("service.category", string="Category")
    issue_date = fields.Date(string="Issue Date")
    state = fields.Selection([('complete', 'Complete'),
                              ('in-complete', 'Pending')], string="Status")
    user_id = fields.Many2one('res.users', string="By")


class VehicalDivison(models.Model):
    """Model Vehicle Divison."""


    _name = 'vehicle.divison'
    _description = 'Vehicle Division'

    code = fields.Char(string='Code', size=3)
    name = fields.Char(string='Name', required=True)


class FleetVehicleModelBrand(models.Model):
    """Model Fleet Vehicle Model Brand."""

    _inherit = 'fleet.vehicle.model.brand'

    name = fields.Char(string='Make', size=64, required=True)


class InsuranceType(models.Model):
    """Model Insurance Type."""

    _name = 'insurance.type'
    _description = 'Vehicle Insurence Type'

    name = fields.Char(string='Name')


class VehicleType(models.Model):
    """Model Vehicle Type."""

    _name = 'vehicle.type'
    _description = 'Vehicle Type'


    code = fields.Char(string='Code', size=10)
    name = fields.Char(string='Name', size=64, required=True)


class DamageTypes(models.Model):
    _name = "damage.types"
    _description = "Damage Types"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")


class NextIncrementNumber(models.Model):
    """Model Next Increment NUmber."""

    _name = 'next.increment.number'
    _description = 'Next Increment Number'

    name = fields.Char(string='Name', size=64)
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle Id')
    number = fields.Float(string='Odometer Increment')


class NextServiceDays(models.Model):
    """Model Next Service Days."""

    _name = 'next.service.days'
    _description = 'Next Service days'

    name = fields.Char(string='Name', translate=True)
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle Id')
    days = fields.Integer(string='Days')


class VehicleType(models.Model):
    """Model Vehicle Type."""

    _name = 'vehicle.type'
    _description = 'Vehicle Type'


    code = fields.Char(string='Code', size=10)
    name = fields.Char(string='Name', size=64, required=True)



# class IrAttachment(models.Model):
#     """Model Ir Attachment."""
#
#     _inherit = 'ir.attachment'
#
#     attachment_id = fields.Many2one('fleet.vehicle')
#     attachment_id_2 = fields.Many2one('fleet.vehicle')
