

from odoo import fields, models


class ProductAssets(models.Model):
    _inherit = "product.template"

    asset_id=fields.One2many(
        comodel_name="inventory_services.assets",
        inverse_name="product_id",
        string="Assets",
    )