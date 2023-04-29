from odoo import models, api


class TimesheetXlsx(models.AbstractModel):
    _name = "report.purchase_line_import_sample"
    _inherit = "report.report_xlsx.abstract"
    _description = "Purchase Line Import - Sample File"

    @api.model
    def _get_report_values(self, data=None):
        return {"report_data": data}

    def generate_xlsx_report(self, workbook, data, records):
        sheet = workbook.add_worksheet("Order Lines")
        sheet.set_column(0, 4, 20)

        bold = workbook.add_format({"bold": True})

        sheet.write(0, 0, "Product", bold)
        sheet.write(0, 1, "Internal Description", bold)
        sheet.write(0, 2, "Description", bold)
        sheet.write(0, 3, "Quantity", bold)
        sheet.write(0, 4, "Unit Price", bold)

        SAMPLE_DATA = [
            {
                "product": "Office Lamp",
                "default_code": "FURN_8888",
                "description": "Office Lamp",
                "quantity": 9,
                "unit_price": 58.00,
            },
            {
                "product": "Office Chair",
                "default_code": "FURN_7777",
                "description": "Office Chair",
                "quantity": 3,
                "unit_price": 65.00,
            },
            {
                "product": "Three-Seat Sofa",
                "default_code": "FURN_8999",
                "description": "Three-Seat Sofa",
                "quantity": 4,
                "unit_price": 154.50,
            },
        ]

        row = 1
        for data in SAMPLE_DATA:
            sheet.write(row, 0, data["product"])
            sheet.write(row, 1, data["default_code"])
            sheet.write(row, 2, data["description"])
            sheet.write(row, 3, data["quantity"])
            sheet.write(row, 4, data["unit_price"])
            row += 1
