from odoo import models, fields, api

class SaleOrder(models.Model):
  _inherit = 'sale.order'

  @api.multi
  def open_url(self):
    url = 'https://www.youtube.com/watch?v=DlaanycDbQE'
    return {
      'type': 'ir.actions.act_url',
      'url': url,
      'target': 'new',
    }