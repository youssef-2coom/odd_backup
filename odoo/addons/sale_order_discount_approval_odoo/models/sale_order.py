# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError



class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('order_line.price_total')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = amount_discount = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
                amount_discount += (line.product_uom_qty * line.price_unit * line.discount) / 100
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_discount': amount_discount,
                'amount_total': amount_untaxed + amount_tax,
            })

    discount_type = fields.Selection([('amount', 'Amount')], string='Discount type',
                                     readonly=True,
                                     states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                     default='amount')


    discount_rate = fields.Float('Discount Rate', digits=dp.get_precision('Account'),
                                 readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all',
                                     track_visibility='always')
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all',
                                 track_visibility='always')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all',
                                   track_visibility='always')
    amount_discount = fields.Monetary(string='Discount', store=True, readonly=True, compute='_amount_all',
                                      digits=dp.get_precision('Account'), track_visibility='always')

    @api.onchange('discount_type', 'discount_rate', 'order_line')
    def supply_rate(self):
        for order in self:
            if order.discount_type == 'percent':
                for line in order.order_line:
                    line.discount = order.discount_rate
            else:
                total = discount = 0.0
                for line in order.order_line:
                    total += round((line.product_uom_qty * line.price_unit))
                if order.discount_rate != 0:
                    discount = (order.discount_rate / total) * 100
                else:
                    discount = order.discount_rate
                for line in order.order_line:
                    line.discount = discount
                    # print(line.discount)
                    #new_sub_price = amount of discount
                    new_sub_price = (line.price_unit * (discount/100))
                    line.total_discount = line.price_unit - new_sub_price

    def _prepare_invoice(self, ):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({
            'discount_type': self.discount_type,
            'discount_rate': self.discount_rate,
        })
        return invoice_vals

    def button_dummy(self):

        self.supply_rate()
        return True

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    discount = fields.Float(string='Discount (%)', digits=(16, 20), default=0.0)
    total_discount = fields.Float(string="Total Discount", default=0.0, store=True)





class SaleOrderDiscount(models.Model):
    _inherit = 'sale.order'
    state = fields.Selection(
        selection_add=[('waiting_for_approval', 'Waiting For Approval'),
                       ('sale',)])
    approval_user_id = fields.Many2one('res.users',
                                       string='Discount Approved By')

    @api.depends('order_line.price_total')
    def action_confirm(self):
        """Method for confirming the sale order discount and sending mail for the approvar if approval limit crossed"""

        res = super(SaleOrderDiscount, self).action_confirm()
        to_approve = False


        discount_vals = self.order_line.mapped('total_discount')

        approval_users = self.env.ref(
            'sale_order_discount_approval_odoo.group_approval_manager').users
        user_discount = self.env.user.allow_discount



        if self.env.user.discount_control == True:
            for order in self:
                for line in order.order_line:
                    if line.price_unit - line.total_discount > user_discount:
                        to_approve = True
                        break


        #if to_approve == True and self.env.user.user_discount < (line.price_unit - line.total_discount)

        # @api.constrains('user_discount')
        # def _check_if_user_allowed(self):
        #     if self.to_approve == True and self.user_discount < (line.price_unit - line.total_discount):
        #         to_approve = True
        #         raise ValidationError("Sorry but you're not allowed to confirm on such a high discount.")

        if to_approve == True:
            display_id = self.id
            action_id = self.env.ref(
                'sale.action_quotations_with_onboarding').id
            base_url = self.env['ir.config_parameter'].sudo().get_param(
                'web.base.url')
            redirect_link = "/web#id=%s&cids=1&menu_id=178&action=%s" \
                            "&model" \
                            "=sale.order&view_type=form" % (
                                display_id, action_id)
            url = base_url + redirect_link
            for user in approval_users:
                mail_body = """
                <p>Hello,</p>
                       <p>New sale order '%s' Created with Discount by '%s' 
                       need your approval on it.</p>
                       <p>To Approve, Cancel Order, Click on the Following 
                       Link:
                       <a href='%s' style="display: inline-block; 
                       padding: 10px; text-decoration: none; font-size: 12px; background-color: #875A7B; color: #fff; border-radius: 5px;"><strong>Click Me</strong></a>
                       </p>
                       <p>Thank You.</p>""" % (self.name, self.env.user.name,
                                               url)
                mail_values = {
                    'subject': "'%s' Discount Approval Request" % (self.name),
                    'body_html': mail_body,
                    'email_to': user.partner_id.email,
                    'model': 'sale.order',
                }
                mail_id = self.env['mail.mail'].sudo().create(mail_values)
                mail_id.sudo().send()
            self.state = 'waiting_for_approval'
        return res

    # def action_waiting_approval(self):
    #     """Method for approving the sale order discount"""
    #     self.approval_user_id = self.env.user.id
    #     self.state = 'sale'



    def action_waiting_approval(self):
        """Method for approving the sale order discount"""
        if self.env.user.allow_discount > self.amount_discount:
            self.state = 'sale'
        else:
            raise ValidationError("Sorry but you're not allowed to confirm on such a high discount.")
                # to_approve = True


