# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, tools, _
from odoo.tools.float_utils import float_round

class Employee(models.Model):
    _inherit = "hr.employee"
    
    
    def _get_paid_remaining_leaves(self):
        """ Helper to compute the remaining leaves for the current employees
            :returns dict where the key is the employee id, and the value is the remain leaves
        """
        self._cr.execute("""
            SELECT
                sum(h.number_of_days) AS days,
                h.employee_id
            FROM
                (
                    SELECT holiday_status_id, number_of_days,
                        state, employee_id
                    FROM hr_leave_allocation
                    UNION
                    SELECT holiday_status_id, (number_of_days * -1) as number_of_days,
                        state, employee_id
                    FROM hr_leave
                ) h
                join hr_leave_type s ON (s.id=h.holiday_status_id)
            WHERE
                h.state='validate' AND
                (s.allocation_type='fixed' OR s.allocation_type='fixed_allocation')AND s.unpaid=False AND
                h.employee_id in %s
            GROUP BY h.employee_id""", (tuple(self.ids),))
        return dict((row['employee_id'], row['days']) for row in self._cr.dictfetchall())

    def _compute_paid_remaining_leaves(self):
        remaining = self._get_paid_remaining_leaves()
        for employee in self:
            employee.remaining_paid_leaves = float_round(remaining.get(employee.id, 0.0), precision_digits=2)
            
    remaining_paid_leaves = fields.Float(
        compute='_compute_paid_remaining_leaves', string='Remaining Paid Leaves',
        help='Total number of legal leaves allocated to this employee, change this value to create allocation/leave request. '
             'Total based on all the leave types without overriding limit.')
    
    