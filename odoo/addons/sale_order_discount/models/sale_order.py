# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ResUsers(models.Model):
    _inherit = 'res.users'

    max_allow_discount = fields.Float('Maximum Allow Discount', copy=False)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    discount_amount = fields.Float('Discount Amt.')

    @api.onchange('discount_amount')
    def onchange_discount_amount(self):
        user_id = self.env.user
        for line in self:
            if line.discount_amount:
                if line.discount_amount > user_id.max_allow_discount:
                    raise UserError(f"You are not allowed to give this amount of discount in {line.product_id.name}!")
                else:
                    line.discount = (line.discount_amount / (line.product_uom_qty * line.price_unit)) * 100


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        user_id = self.env.user
        res = super(SaleOrder, self).action_confirm()
        for line in self.order_line:
            if line.discount_amount:
                if line.discount_amount > user_id.max_allow_discount:
                    raise UserError(f"You are not allowed to give this amount of discount in {line.product_id.name}!")
        return res
