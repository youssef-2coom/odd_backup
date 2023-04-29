class SalesReport(http.Controller):
   @http.route(['/sales/report'], type="http", auth="public", website=True)
   def sale_report(self, **kw):
       report = request.env['portal.sales.report'].sudo().search([])
       values = {
           'datas': report, }
       return request.render("your_module.sale_report_page", values)