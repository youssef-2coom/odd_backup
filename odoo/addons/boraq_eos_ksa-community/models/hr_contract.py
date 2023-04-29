from odoo import api, fields, models, tools, _
from calendar import monthrange
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class Contract(models.Model):
    _inherit = "hr.contract"
    _description = 'Employee'
    
    
    end_contract = fields.Boolean("End Of Contract?")
    eos_reason = fields.Selection([('resign','Resign'),('terminate','Terminate'),('endcontract','End of Contract')],string="Reason of ending the contract")
    service_month = fields.Integer("Service Period(Month)")
    service_day = fields.Integer("Service Period(Day)")
    service_year = fields.Float("Service Period(Year)")
    
    @api.model
    def create(self,vals):
        if vals.get('end_contract'):
            vals.update({'date_end':datetime.today()})
        if vals.get('date_start',False) and vals.get('date_end',False):
            date_diff = relativedelta(self.date_end, self.date_start)
            day = date_diff.days
            month = date_diff.months
            year = date_diff.years
            year_day = 0.0
            if day > 0:
                year_day = day /365
            year_month = 0.0
            if month > 0:
                year_month = month / 12
            total_year = year + year_day + year_month
            vals.update({'service_day':day,
                        'service_month':month,
                        'service_year':total_year})
        return super(Contract,self).create(vals)
    
    def write(self,vals):
        if vals.get('end_contract'):
            vals.update({'date_end':datetime.today()})
        if self.date_start and self.date_end:
            date_diff = relativedelta(self.date_end, self.date_start)
            day = date_diff.days
            month = date_diff.months
            year = date_diff.years
            
            year_day = 0.0
            if day > 0:
                year_day = day /365
            year_month = 0.0
            if month > 0:
                year_month = month / 12
            total_year = year + year_day + year_month
            vals.update({'service_day':day,
                        'service_month':month,
                        'service_year':total_year})
        return super(Contract,self).write(vals)
    
    
    
#     @api.onchange('end_contract')
#     def end_contract_msg(self):    
#         if self.end_contract:
#             return {
#                 'Information': {
#                     'title': 'Information Massage',
#                     'message': 'We will set today date as End Date of Service',
#                 }
#             }