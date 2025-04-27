# -*- coding: utf-8 -*-

# from odoo import models, fields, api

import json
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Assets(models.Model):
    _name = 'inventory_services.assets'
    _description = 'Assets to products'

    name = fields.Char(
        string='Asset Name',
        required=True,
        help='Name of the asset.'
    )

    description = fields.Text(
        string='Description',
        help='Detailed description of the asset.'
    )

    assets_names = fields.Json(
        string='Asset Images',
        default=list,
        help='List of image file names or URLs associated with this asset.'
    )

    product_id = fields.Many2one(
        comodel_name='product.template',
        string='Product',
        required=True,
        help='Product associated with this asset.',
    )

    @api.constrains('assets_names')
    def _check_assets_names(self):
        for record in self:
            assets = record.assets_names

            print("Assets Names:", assets)
            if isinstance(assets, str):
                try:
                    assets = json.loads(assets)
                except json.JSONDecodeError:
                    raise ValidationError("El formato de 'Assets Images' no es un JSON válido.")

            if not isinstance(assets, list):
                raise ValidationError("El campo 'Assets Images' debe ser una lista de nombres de imágenes.")

            for img in assets:
                if not isinstance(img, str):
                    raise ValidationError("Cada elemento en 'Assets Images' debe ser una cadena de texto (nombre de archivo o URL).")


