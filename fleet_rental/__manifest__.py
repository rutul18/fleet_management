{
    'name': 'Fleet Vehicle Rent',
    'version': '1.0',
    'depends': ['fleet', 'account', 'base', 'account'],
    'author': 'Rutul ',
    'category': 'Management',
    'summary': """Rental Vehicle Management System
            This module provides fleet rent features.""",
    'description': """
            Rental Vehicle Management System
            This module provides fleet rent features..
         """,
    'data': [
                'security/ir.model.access.csv',
                'data/ir_sequence_data.xml',
                'wizard/view_close_reason.xml',
                'views/view_fleet_vehicle_rent.xml',
                'views/vehicle_res_user.xml',
                'views/view_fleet_extends.xml',
                'views/view_fleet_vehicle_account.xml',
             ],

    'auto_install': False,
    'installable': True,
}