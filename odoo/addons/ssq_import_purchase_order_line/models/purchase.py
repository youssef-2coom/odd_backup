from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def import_lines(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Import Order Lines",
            "res_model": "wizard.import.purchase.line",
            "view_mode": "form",
            "target": "new",
            "context": {"default_purchase_id": self.id},
        }
