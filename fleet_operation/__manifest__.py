{
    'name': 'Fleet Vehicle operation',
    'version': '1.0',
    'depends': ['fleet', 'account', 'base'],
    'author': 'Rutul ',
    'category': 'Management',
    'summary': """ Vehicle Management System
            This module provides fleet Operation features.""",
    'description': """
            This module provides fleet Operation features..
         """,
    'data': [
                'wizard/123.xml',
                'views/view_fleet_extend.xml',
                'views/view_fleet_vehicle_service.xml',
                'views/view_fleet_vehicle_account_operation.xml',
                'data/vehicle_service_sequence.xml'
             ],

    'auto_install': False,
    'installable': True,
}