{
    'name': 'Delivery status on sale order',
    'version': '16.0',
    'category': 'Sale',
    'summery': 'Delivery status on sale order',
    'author': 'INKERP',
    'website': "https://www.INKERP.com",
    'depends': ['sale', 'sale_stock'],

    'data': [
        'views/sale_order_view.xml',
    ],

    'images': ['static/description/banner.png'],
    'license': "OPL-1",
    'installable': True,
    'application': True,
    'auto_install': False,
}
