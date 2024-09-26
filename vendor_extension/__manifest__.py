{
    'name': "Vendor Extension App",
    'version': '1.0',
    'depends': ['product_extension','purchase'],
    'description': """ Vendor Extension Module """,
    'data': ['security/ir.model.access.csv',
             'data/vendor_status_data.xml',
             'data/compliances_data.xml',
             'views/res.partner_view.xml',
             'views/product_supplier_info_view.xml',
             'views/vendor_status_view.xml',
             'views/compliances_view.xml'],
    'installable': True,
    'application': True,
    'sequence': -2,
    'license': 'LGPL-3'
}
