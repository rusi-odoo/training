# -*- coding: utf-8 -*-
{
    'name': "aphora_kaja_food",
    'description': """
    """,

    'author': "Aphora GmbH",
    'website': "https://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '17.0.1.1',
    'depends': ['sale_management', 'mrp_maintenance', 'quality_control', 'documents', 'purchase', 'stock_delivery', 'product_expiry'],
    'data': [
        'security/ir.model.access.csv',
        'data/report_lot_label.xml',
        'data/report_paperformat_data.xml',
        'report/ir_actions_report_templates.xml',
        'report/purchase_order_template.xml',
        'report/report_deliveryslip.xml',
        'report/report_invoice.xml',
        'report/report_stockpicking_operations.xml',
        'report/mrp_production_templates.xml',
        'report/product_reports.xml',
        'wizard/aphora_time_tracking_wizard_view.xml',

        'views/sale_order_view.xml',
        'views/mrp_production_views.xml',
        'views/documents_document_view.xml',
        'views/mrp_workcenter_views.xml',
        'views/stock_picking_views.xml',
        'views/product_view.xml',
        'views/aphora_product_category.xml',
        'views/stock_move_views.xml',
        'views/mrp_workorder_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'aphora_kaja_food/static/src/document_view/documents_inspector.js',
        ],
    },
    'license': 'AGPL-3',
}
