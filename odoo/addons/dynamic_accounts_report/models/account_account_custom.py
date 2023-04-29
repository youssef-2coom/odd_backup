from odoo import models, api


class AccountAccountCustom(models.Model):
    _inherit = 'account.account'

    @api.model
    def create(self, vals):
        res = super(AccountAccountCustom, self).create(vals)
        if res.account_type.startswith("asset"):
            for record in self.env['account.financial.report'].search(
                    [('type', '=', 'account_type')]):
                if record.get_metadata()[0].get(
                        'xmlid') == 'base_accounting_kit.account_financial_report_assets0':
                    record.write({"account_ids": [(4, res.id)]})
        elif res.account_type.startswith(
                "liability") or res.account_type == "equity":
            for record in self.env['account.financial.report'].search(
                    [('type', '=', 'account_type')]):
                if record.get_metadata()[0].get(
                        'xmlid') == 'base_accounting_kit.account_financial_report_liability0':
                    record.write({"account_ids": [(4, res.id)]})
        elif res.account_type in ['expense', 'expense_depreciation']:
            for record in self.env['account.financial.report'].search(
                    [('type', '=', 'account_type')]):
                if record.get_metadata()[0].get(
                        'xmlid') == 'base_accounting_kit.account_financial_report_expense0':
                    record.write({"account_ids": [(4, res.id)]})
        elif res.account_type == "expense_direct_cost":
            for record in self.env['account.financial.report'].search(
                    [('type', '=', 'account_type')]):
                if record.get_metadata()[0].get(
                        'xmlid') == 'base_accounting_kit.financial_report_cost_of_revenue':
                    record.write({"account_ids": [(4, res.id)]})
        elif res.account_type in ['income', 'equity_unaffected']:
            for record in self.env['account.financial.report'].search(
                    [('type', '=', 'account_type')]):
                if record.get_metadata()[0].get(
                        'xmlid') == 'base_accounting_kit.account_financial_report_operating_income0':
                    record.write({"account_ids": [(4, res.id)]})
        elif res.account_type == 'income_other':
            for record in self.env['account.financial.report'].search(
                    [('type', '=', 'account_type')]):
                if record.get_metadata()[0].get(
                        'xmlid') == 'base_accounting_kit.account_financial_report_other_income0':
                    record.write({"account_ids": [(4, res.id)]})
        return res

    @api.onchange('account_type')
    def onchange_account_type(self):
        for record in self.env['account.financial.report'].search(
                [('type', '=', 'account_type')]):
            for rec in record.account_ids:
                if rec.id == self._origin.id:
                    record.write({"account_ids": [(3, rec.id)]})
                    if self.account_type.startswith("asset"):
                        for record1 in self.env[
                            'account.financial.report'].search(
                            [('type', '=', 'account_type')]):
                            if record1.get_metadata()[0].get(
                                    'xmlid') == 'base_accounting_kit.account_financial_report_assets0':
                                record1.write(
                                    {"account_ids": [(4, self._origin.id)]})
                    elif self.account_type.startswith(
                            "liability") or self.account_type == "equity":
                        for record1 in self.env[
                            'account.financial.report'].search(
                            [('type', '=', 'account_type')]):
                            if record1.get_metadata()[0].get(
                                    'xmlid') == 'base_accounting_kit.account_financial_report_liability0':
                                record1.write(
                                    {"account_ids": [(4, self._origin.id)]})
                    elif self.account_type in ['expense',
                                               'expense_depreciation']:
                        for record1 in self.env[
                            'account.financial.report'].search(
                            [('type', '=', 'account_type')]):
                            if record1.get_metadata()[0].get(
                                    'xmlid') == 'base_accounting_kit.account_financial_report_expense0':
                                record1.write(
                                    {"account_ids": [(4, self._origin.id)]})
                    elif self.account_type == "expense_direct_cost":
                        for record1 in self.env[
                            'account.financial.report'].search(
                            [('type', '=', 'account_type')]):
                            if record1.get_metadata()[0].get(
                                    'xmlid') == 'base_accounting_kit.financial_report_cost_of_revenue':
                                record1.write(
                                    {"account_ids": [(4, self._origin.id)]})
                    elif self.account_type in ['income', 'equity_unaffected']:
                        for record1 in self.env[
                            'account.financial.report'].search(
                            [('type', '=', 'account_type')]):
                            if record1.get_metadata()[0].get(
                                    'xmlid') == 'base_accounting_kit.account_financial_report_operating_income0':
                                record1.write(
                                    {"account_ids": [(4, self._origin.id)]})
                    elif self.account_type == 'income_other':
                        for record1 in self.env[
                            'account.financial.report'].search(
                            [('type', '=', 'account_type')]):
                            if record1.get_metadata()[0].get(
                                    'xmlid') == 'base_accounting_kit.account_financial_report_other_income0':
                                record1.write(
                                    {"account_ids": [(4, self._origin.id)]})
