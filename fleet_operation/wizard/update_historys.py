from odoo import fields, models
from datetime import date, datetime



class UpdateEngineInfo(models.TransientModel):
    """Update Engine Info."""
    print ("::::::::::::::::::::::::::::::::")
    _name = 'update.engine.info'
    _description = 'Update Engine Info'

    workorder_id = fields.Many2one('fleet.vehicle.log.services', string='Work Order')
    previous_engine_no = fields.Char(string='Previous Engine No', size=64, translate=True)
    new_engine_no = fields.Char(string="New Engine No", size=64, translate=True)
    changed_date = fields.Date(string='Change Date', default=datetime.now().date())
    note = fields.Text(string='Notes', translate=True)
    temp_bool = fields.Boolean(default=True, string='Temp Bool for making previous color readonly')
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle")


class UpdateColorInfo(models.TransientModel):
    """Update Color Info."""

    print("::::::::::::::::11::::::::::::::::")
    _name = 'update.color.info'
    _description = 'Update Color Info'

    workorder_id = fields.Many2one('fleet.vehicle.log.services', string='Work Order')
    previous_color_id = fields.Many2one('color.color', string="Previous Color")
    current_color_id = fields.Many2one('color.color', string="New Color")
    changed_date = fields.Date(string='Change Date', default=datetime.now().date())
    note = fields.Text(string='Notes', translate=True)
    temp_bool = fields.Boolean(default=True, string='Temp Bool for making previous color readonly')
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle")




class UpdateVinInfo(models.TransientModel):
    """Update Vin Info."""

    print("::::::::::::::::11::22::::::::::::::")
    _name = 'update.vin.info'
    _description = 'Update Vin Info'

    workorder_id = fields.Many2one('fleet.vehicle.log.services', string='Work Order')
    previous_vin_no = fields.Char(string='Previous Vin No', size=124)
    new_vin_no = fields.Char(string="New Vin No", size=124)
    changed_date = fields.Date(default=datetime.now().date(), string='Change Date')
    note = fields.Text(string='Notes', translate=True)
    temp_bool = fields.Boolean(default=True, string='Temp Bool for making previous color readonly')
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle")



class UpdateTireInfo(models.TransientModel):
    """Update Tire Info."""

    print("::::::::::::::::11::::::::333::::::::")
    _name = 'update.tire.info'
    _description = 'Update Tire Info'

    previous_tire_size = fields.Char(string='Previous Tire Size', size=124)
    new_tire_size = fields.Char(string="New Tire Size", size=124)
    previous_tire_sn = fields.Char(string='Previous Tire S/N', size=124)
    new_tire_sn = fields.Char(string="New Tire S/N", size=124)
    previous_tire_issue_date = fields.Date(string='Previous Tire Issuance Date')
    new_tire_issue_date = fields.Date(string='New Tire Issuance Date')
    changed_date = fields.Date(string='Change Date', default=datetime.now().date())
    note = fields.Text('Notes', translate=True)
    temp_bool = fields.Boolean(default=True, string='Temp Bool for making previous Tire info readonly')
    workorder_id = fields.Many2one('fleet.vehicle.log.services', string='Work Order')
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle")



class UpdateBatteryInfo(models.TransientModel):
    """Update Battery Info."""

    print("::::::::::::::::11:::::::ddddd:::::::::")
    _name = 'update.battery.info'
    _description = 'Update Battery Info'

    previous_battery_size = fields.Char(string='Previous Battery Size', size=124)
    new_battery_size = fields.Char(string="New Battery Size", size=124)
    previous_battery_sn = fields.Char(string='Previous Battery S/N', size=124)
    new_battery_sn = fields.Char(string="New Battery S/N", size=124)
    previous_battery_issue_date = fields.Date(string='Previous Battery Issuance Date')
    new_battery_issue_date = fields.Date(string='New Battery Issuance Date')
    changed_date = fields.Date(string='Change Date', default=datetime.now().date())
    note = fields.Text(string='Notes', translate=True)
    temp_bool = fields.Boolean(default=True, string='Temp Bool for making previous Battery info readonly')
    workorder_id = fields.Many2one('fleet.vehicle.log.services', string='Work Order')
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle")



