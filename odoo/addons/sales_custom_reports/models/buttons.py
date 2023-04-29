# In your new module, define a new model that extends the SaleOrder model
from odoo import models, fields, api


class SaleOrderCustom(models.Model):
    _inherit = 'sale.order'

    # Define a new button
    @api.multi
    def custom_button(self):
        # Do something when the button is clicked
        print('The Devexpress report should go up here!')
