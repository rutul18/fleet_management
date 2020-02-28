import time
from datetime import date, datetime, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, Warning
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, misc



class FleetVehicleLogServices(models.Model):
    """Fleet Vehicle Log Services Model."""

    _inherit = 'fleet.vehicle.log.services'
    _description = "Fleet vehicle service log extend fields"


    def action_create_invoice(self):
        """"create Invoice method"""
        print("\:::::Invoice:::", self)


    def action_return_invoice(self):
        """"Return Invoice method"""
        print("\:::::Invoice:::", self)


    def action_confirm(self):
        """"Confirm Button Method"""
        print("/n:::::Invoice:::", self)
        sequence = self.env['ir.sequence'].next_by_code(
            'service.order.sequence')
        mod_obj = self.env['ir.model.data']
        cr, uid, context = self.env.args
        context = dict(context)
        for work_order in self:
            print("/n:::::work order:::", work_order)
            if work_order.vehicle_id:
                if work_order.vehicle_id.state == 'write-off':
                    raise Warning(_("You can\'t confirm this \
                                  work order which vehicle is in write-off state!"))
                elif work_order.vehicle_id.state == 'in_progress':
                    raise Warning(_("Previous work order is not \
                                  complete, complete that work order first than \
                                      you can confirm this work order!"))
                elif work_order.vehicle_id.state == 'draft' or \
                        work_order.vehicle_id.state == 'complete':
                    raise Warning(_("Confirm work order can only \
                              when vehicle status is in Inspection or Released!"))
                work_order.vehicle_id.write({
                    'state': 'in_progress',
                    'last_change_status_date': date.today(),
                    'work_order_close': False})
            work_order.write({'state': 'confirm', 'name': sequence,
                              'date_open':
                                  time.strftime(DEFAULT_SERVER_DATE_FORMAT)})
            model_data_ids = mod_obj.search([
                ('model', '=', 'ir.ui.view'),
                ('name', '=', 'continue_pending_repair_form_view')])
            resource_id = model_data_ids.read(['res_id'])[0]
            context.update({'work_order_id': work_order.id,
                            'vehicle_id': work_order.vehicle_id and
                                          work_order.vehicle_id.id or False})
            self.env.args = cr, uid, misc.frozendict(context)
            if work_order.vehicle_id:
                for pending_repair in \
                        work_order.vehicle_id.pending_repair_type_ids:
                    if pending_repair.state == 'in-complete':
                        return {
                            'name': _('Previous Repair Types'),
                            'context': self._context,
                            'view_type': 'form',
                            'view_mode': 'form',
                            'res_model': 'continue.pending.repair',
                            'views': [(resource_id, 'form')],
                            'type': 'ir.actions.act_window',
                            'target': 'new',
                        }
        return True

    def action_done(self):
        """"Done Button Method"""
        print("\:::::Invoice:::", self)


    def action_reopen(self):
        """Re-open Button Method"""
        print("\:::::Invoice:::", self)


    wono_id = fields.Integer(string='WONo', help="Take this field for data migration")
    id = fields.Integer(string='ID')
    purchaser_id = fields.Many2one('res.partner', string='Purchaser', related='vehicle_id.driver_id')
    name = fields.Char(string='Work Order', size=32, readonly=True, copy=False, default="New")
    fmp_id = fields.Char(string="Vehicle ID", size=64, related='vehicle_id.name')
    wo_tax_amount = fields.Float(string='Tax', readonly=True)
    priority = fields.Selection([('normal', 'NORMAL'), ('high', 'HIGH'),
                                 ('low', 'LOW')], default='normal',
                                string='Work Priority')
    date_complete = fields.Date(string='Issued Complete ', help='Date when the service is completed')
    date_open = fields.Date(string='Open Date',
                            help="When Work Order \
                                        will confirm this date will be set.")
    date_close = fields.Date(string='Date Close', help="Closing Date of Work Order")
    closed_by = fields.Many2one('res.users', string='Closed By')
    etic = fields.Boolean(string='Estimated Time',  help="Estimated Time In Completion", default=True)
    wrk_location_id = fields.Many2one('stock.location', string='Location ', readonly=True)
    wrk_attach_ids = fields.One2many('ir.attachment', 'wo_attachment_id', string='Attachments')
    task_ids = fields.One2many('service.task', 'main_id', string='Service Task')
    parts_ids = fields.One2many('task.line', 'fleet_service_id', string='Parts')
    note = fields.Text(string='Log Notes')
    date_child = fields.Date(related='cost_id.date', string='Cost Date', store=True)
    sub_total = fields.Float(string='Total Parts Amount', store=True)
    state = fields.Selection([('draft', 'New'),
                              ('confirm', 'Open'), ('done', 'Done'),
                              ('cancel', 'Cancel')], string='Status',
                             default='draft', readonly=True)
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')
    delivery_id = fields.Many2one('stock.picking', string='Delivery Reference', readonly=True)
    team_id = fields.Many2one('res.partner', string="Teams")
    maintenance_team_id = fields.Many2one("stock.location", string="Team")
    next_service_date = fields.Date(string='Next Service Date')
    next_service_odometer = fields.Float(string='Next Odometer Value', readonly=True)
    repair_line_ids = fields.One2many('service.repair.line', 'service_id', string='Repair Lines')
   # old_parts_incoming_ship_ids = fields.One2many('stock.picking', 'work_order_old_id', string='Old Returned', readonly=True)
    #reopen_return_incoming_ship_ids = fields.One2many('stock.picking', 'work_order_reopen_id', string='Reopen Returned',
            #                                          readonly=True)
   # out_going_ids = fields.One2many('stock.picking', 'work_order_out_id', string='Out Going', readonly=True)
    vechical_type_id = fields.Many2one('vehicle.type', string='Vechical Type')
    # open_days = fields.Char(compute="_get_open_days", string="Open Days")
    already_closed = fields.Boolean("Already Closed?")
    total_parts_line = fields.Integer(string='Total Parts')
    is_parts = fields.Boolean(string="Is Parts Available?")
    from_migration = fields.Boolean('From Migration')
    main_type = fields.Selection([('vehicle', 'Vehicle'),
                                  ('non-vehicle', ' Non-Vehicle')],
                                 string='Main Type')
    f_brand_id = fields.Many2one('fleet.vehicle.model.brand', string='Make')
    vehical_division_id = fields.Many2one('vehicle.divison', string='Division')
   # vechical_location_id = fields.Many2one(related="vehicle_id.vehicle_location_id", string='Registration State')
    odometer = fields.Float(string='Last Odometer', help='Odometer measure of the vehicle at the moment of this log')
    service_amount = fields.Float(string="Total Service Amount")
    source_service_id = fields.Many2one('fleet.vehicle.log.services', string="Service", copy=False)
    invoice_count = fields.Integer(string="Invoice Count")
    return_inv_count = fields.Integer(string="Return Invoice")
    amount_receive = fields.Boolean( string="Invoice Receive")
    amount_return = fields.Boolean(string="Invoice Return")
    service_invoice_id = fields.One2many('account.invoice', 'vehicle_service_id', string="Service Invoice")
    service_ref_invoice_id = fields.One2many('account.invoice', 'vehicle_service_id', string="Service Refund Invoice")



class IrAttachment(models.Model):
    """Ir Attachmentmodel."""

    _inherit = 'ir.attachment'

    wo_attachment_id = fields.Many2one('fleet.vehicle.log.services')


class ServiceTask(models.Model):
    """Service Task Model."""

    _name = 'service.task'
    _description = 'Maintenance of the Task '

    main_id = fields.Many2one('fleet.vehicle.log.services',
                              string='Maintanace Reference')
    type = fields.Many2one('fleet.service.type', string='Type')
    total_type = fields.Float(string='Cost', readonly=True, default=0.0)
    product_ids = fields.One2many('task.line', 'task_id', string='Product')
    maintenance_info = fields.Text(string='Information', translate=True)


class TaskLine(models.Model):
    """Task Line Model."""

    _name = 'task.line'
    _description = 'Task Line'

    task_id = fields.Many2one('service.task',
                              string='task reference')
    fleet_service_id = fields.Many2one('fleet.vehicle.log.services',
                                       string='Vehicle Work Order')
    product_id = fields.Many2one('product.product', string='Part')
    qty_hand = fields.Float(string='Qty on Hand',
                            help='Quantity on Hand')
    qty = fields.Float(string='Used', default=1.0)
    product_uom = fields.Many2one('uom.uom', string='UOM')
    price_unit = fields.Float(string='Unit Cost')
    total = fields.Float(string='Total Cost')
    date_issued = fields.Datetime(string='Date issued')
    issued_by = fields.Many2one('res.users', string='Issued By',
                                default=lambda self: self._uid)
    is_deliver = fields.Boolean(string="Is Deliver?")


class ServiceRepairLine(models.Model):
    """Service Repair Line."""

    _name = 'service.repair.line'
    _description = 'Service Repair Line'


    service_id = fields.Many2one('fleet.vehicle.log.services',
                                 ondelete='cascade')
    repair_type_id = fields.Many2one('repair.type', string='Repair Type')
    categ_id = fields.Many2one('service.category', string='Category')
    issue_date = fields.Date(string='Issued Date ')
    date_complete = fields.Date(related='service_id.date_complete',
                                string="Complete Date")
    target_date = fields.Date(string='Target Completion')
    complete = fields.Boolean(string='Completed')


class RepairType(models.Model):
    """Repair Type."""

    _name = 'repair.type'
    _description = 'Vehicle Repair Type'

    name = fields.Char(string='Repair Type')


class ServiceCategory(models.Model):
    """Service Category Model."""

    _name = 'service.category'
    _description = 'Vehicle Service Category'

    name = fields.Char(string="Service Category")




