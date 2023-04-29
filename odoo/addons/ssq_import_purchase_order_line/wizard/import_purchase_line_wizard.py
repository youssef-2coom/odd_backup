from odoo import fields, models, _
from odoo.exceptions import ValidationError
import xlrd
import base64
import io
import base64


class WizardImportPurchaseLine(models.TransientModel):
    _name = "wizard.import.purchase.line"

    purchase_id = fields.Many2one("purchase.order")
    import_file = fields.Binary("Upload XLSX")
    message = fields.Html("Response")
    message_type = fields.Selection([("import", "Import"), ("success", "Success")], default="import")

    def import_xlsx_file(self):
        if not self.import_file:
            raise ValidationError(_("Please upload a file to import."))
        try:
            inputx = io.BytesIO()
            inputx.write(base64.decodebytes(self.import_file))
            workbook = xlrd.open_workbook(file_contents=inputx.getvalue())
        except TypeError as e:
            raise ValidationError(_("ERROR: {}".format(e)))
        sheet = workbook.sheet_by_index(0)

        message = ""
        order_lines = []
        Product = self.env["product.product"]

        for row in range(1, sheet.nrows):
            product_name = sheet.cell(row, 0).value
            default_code = sheet.cell(row, 1).value
            description = sheet.cell(row, 2).value
            try:
                quantity = float(sheet.cell(row, 3).value)
                unit_price = float(sheet.cell(row, 4).value)
            except Exception as e:
                error_string = "Line " + str(row + 1) + " : " + str(e)
                message += "<p>" + error_string + "</p>"
                continue

            product = Product.search([("default_code", "=", default_code)])
            if not product:
                product = Product.search([("name", "=", product_name), ("purchase_ok", "=", True)], limit=1)
            if not product:
                error_string = "Line " + str(row + 1) + " : Product not found"
                message += "<p>" + error_string + "</p>"
                continue
            order_lines.append(
                (
                    0,
                    0,
                    {
                        "product_id": product.id,
                        "name": description if description else product.name,
                        "product_qty": quantity,
                        "price_unit": unit_price,
                    },
                )
            )
            message_string = "Line " + str(row + 1) + " : Success"
            message += "<p>" + message_string + "</p>"
        self.purchase_id.write({"order_line": order_lines})
        return {
            "type": "ir.actions.act_window",
            "name": "Import Order Lines",
            "res_model": self._name,
            "view_mode": "form",
            "target": "new",
            "context": {"default_message": message, "default_message_type": "success"},
        }

    def download_sample_file(self):
        return self.env.ref("ssq_import_purchase_order_line.import_purchase_line_sample").report_action(self)
