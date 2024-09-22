

{
    'name': 'Br Product Brand in Sale',
    'version': '16.0.1.0.0',
    'category': 'Sales',
    'summary': 'Product Brand in Sales',
    'description': 'Product Brand in Sales,brand,sale, odoo16',
    'author': 'Banibro IT Solutions Pvt Ltd.',
    'company': 'Banibro IT Solutions Pvt Ltd.',
    'website': 'https://banibro.com',
    'images': ['static/description/banner.png',
               'static/description/icon.png',],
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/brand_views.xml',
        'views/sale_report_views.xml'
    ],
    'license': 'AGPL-3',
    'email': "support@banibro.com",
    'installable': True,
    'auto_install': False,
    'application': False,

}
