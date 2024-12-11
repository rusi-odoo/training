{
    "name": "Product Restriction on User",
    'version': "17.0",
    "summary": "This app will restrict multiple Products category for particular user.",
    "depends": ['product', 'sale_management', 'purchase', 'stock'],
    "data": [
        "security/security.xml",
        "views/product_category_view.xml",
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
