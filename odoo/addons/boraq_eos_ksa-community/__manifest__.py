# -*- coding: utf-8 -*-
{
    'name': "End of Service Reward for Saudi Arabia",

    'summary': """This module will help to calculate reward while end of the service as Saudi region.""",
    'description': "End of Service reward calculation depending on Saudi Arabia's laws",
    'author': "Boraq-Group",
    'website': "https://boraq-group.com",
    'category': 'HR',
    'version': '14.0.1.0.0',
    'depends': ['hr', 'hr_holidays', 'hr_payroll_community'],
    'data': [
        'views/hr_contract_view.xml',
        'data/hr_payroll_data.xml',
        'views/hr_employee_view.xml',
        'views/hr_payroll_structure.xml',
    ],
    'images': ['static/description/banner.png'],
    'qweb': [],
    'license': "OPL-1",
    'installable': True,
    'application': True,
    'price': 40,
    'currency': 'EUR',
}
