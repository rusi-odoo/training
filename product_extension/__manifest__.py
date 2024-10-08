{
    'name': "Product Extension App",
    'version': '1.0',
    'depends': ['stock','sale','quality'],
    'description': """ Product Extension Module """,
    'data': ['security/ir.model.access.csv',
             'views/product_status_views.xml',
             'views/product_template_view.xml',
             'views/product_packaging_view.xml',
             'views/product_palletspec.xml',
             'views/product_category_view.xml',
             ],
    'demo':['data/demo.xml'],
    'installable': True,
    'application': True,
    'sequence': -2,
    'license': 'LGPL-3'
}
