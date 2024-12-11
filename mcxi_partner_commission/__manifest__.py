# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "MCXI Partner Commission",
    "version": "17.0.1.0.0",
    "summary": """ MCXI Partner Commission on Sales Order """,
    "author": "Odoo PS",
    "website": "https://www.odoo.com",
    "category": "Customizations",
    "depends": [
        "mcxi_dealer_code",
        "partner_commission",
        "account",
        "sale_management",
        "hr"
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/generate_report_view.xml",
        "views/product_commission_view.xml",
        "views/account_move_views.xml",
        "views/sale_order_views.xml",
        "views/res_partner_views.xml",
    ],
    "application": False,
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
