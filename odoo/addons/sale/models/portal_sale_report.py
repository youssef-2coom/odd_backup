from odoo import models, fields, tools
class SalesReport(models.Model):
   _name = 'portal.sales.report'
   _auto = False
   id = fields.Integer("ID")
   order = fields.Char("Order")
   product = fields.Char("product")
   unit_price = fields.Char("Price")
   quantity = fields.Char("Quantity")
   date = fields.Char("Date")

   def init(self):
       tools.drop_view_if_exists(self.env.cr, 'portal_sales_report')
       self.env.cr.execute("""CREATE OR REPLACE VIEW portal_sales_report AS (select row_number() OVER() AS id, so.name as order,pt.name ->> 'en_US' as product,
              sol.price_unit as unit_price,sol.product_uom_qty as quantity, so.date_order as date from
              sale_order_line as sol left join sale_order as so on sol.order_id=so.id
        left join product_product as pp on sol.product_id = pp.id
        left join product_template as pt on pp.product_tmpl_id =pt.id)""")