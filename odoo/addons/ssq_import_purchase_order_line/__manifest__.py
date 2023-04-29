{
    "name": "Import Purchase Order Line",
    "summary": """
        Import purchase order lines from xlsx file
    """,
    "description": """
        Import purchase order lines from xlsx file
    """,
    "author": "Sanesquare Technologies",
    "website": "https://www.sanesquare.com/",
    "support": "odoo@sanesquare.com",
    "license": "AGPL-3",
    "category": "Uncategorized",
    "version": "16.0.1.0.1",
    "images": ["static/description/app_image.png"],
    "depends": ["purchase", "report_xlsx"],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/purchase_views.xml",
        "wizard/import_purchase_line_wizard_views.xml",
        "report/report_import_purchase_line_sample.xml",
    ],
    "external_dependencies": {"python": ["xlrd"]},
}
