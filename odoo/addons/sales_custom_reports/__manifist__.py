# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'IFRSERP Custom Report',
    'category': 'Sales',
    'summary': 'Devexpress Custom Report',
    'license': 'LGPL-3',

"""
Using this application you can manage Sales Teams with CRM and/or Sales
=======================================================================
 """,
    'website': 'https://www.ifrserp..net',
    'depends': ['Sales'],
    'data': [
        'views/buttons.xml'
        ],

    'installable': True,
    'application': True,
    'auto_install': False,

}
