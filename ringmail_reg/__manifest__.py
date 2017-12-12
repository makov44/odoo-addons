# -*- coding: utf-8 -*-
{
    'name': "Ringmail Registration",

    'summary': """
        Domain registration module.""",

    'description': """
        Enable RingMail For Domain Names
    """,

    'author': "RingMail Inc.",
    'website': "http://www.ringmail.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'communication',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/email_templates_data.xml',
        'views/templates.xml',
        'views/domains_views.xml',
        'views/aliases_views.xml',
        'views/menu_views.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
}