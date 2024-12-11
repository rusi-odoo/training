# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    # Information
    'name': 'Auto Generate Dealer Code',
    'version': '17.0.1.0.0',
    'category': 'Custom Development',
    'summary': 'Automatically generate a 5-digit Dealer Code for new customers',
    'description': """
        This module automates the creation of a 5-digit Dealer Code starting from 5000_ for
        every new customer.
        Task Id - 4260651
    """,

    # Author
    'author': 'Odoo PS',
    'website': 'https://www.odoo.com/',
    'license': 'LGPL-3',

    # Dependency
    'depends': ['contacts'],
    'data': [
        "data/ir_sequence_data.xml",
        "views/res_partner_views.xml",
    ],

    # Other
    'qweb': [],
    'installable': True,
    'auto_install': False,
}
