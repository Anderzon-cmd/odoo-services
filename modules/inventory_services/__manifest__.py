# -*- coding: utf-8 -*-
{
    'name': "Modulo de Servicios de Inventario",

    'summary': "Modulos de servicios de inventario",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/asset.xml',
        'views/receip.xml',
        'views/views.xml',
        'views/templates.xml',
        'menu/assets_menu.xml'
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

