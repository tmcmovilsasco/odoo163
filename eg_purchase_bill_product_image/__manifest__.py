{
    'name': 'Print product image in Purchase',
    'version': '16.0.1.0.0',
    'category': 'Inventory/Purchase',
    'author': 'INKERP',
    'website': "https://www.inkerp.com",
    'summery': 'Check for customer credit on Invoice View/Print',
    'depends': ['purchase', 'account'],

    'data': [
        'reports/account_report_template.xml',
        'reports/purchase_report_template.xml',
        'views/account_move_view.xml',
        'views/purchase_order_view.xml',
    ],

    'images': ['static/description/banner.png'],
    'license': "OPL-1",
    'installable': True,
    'application': True,
    'auto_install': False,
}
