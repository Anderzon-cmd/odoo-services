import requests
from odoo import _, models, fields, api
import base64
import csv
import io

from odoo.exceptions import UserError

class ImportPickingWizard(models.TransientModel):
    _name = 'import.picking.wizard'
    _description = 'Import Picking from File'

    file = fields.Binary(string="Recibo PDF", required=True)
    file_name=fields.Char("Nombre del archivo")

    url=fields.Char(string="URL", required=True, help="Endpoint URL to send the file")


    def action_import_file(self):
        
        if not self.file or not self.url:
            raise UserError(_("Debe proporcionar el archivo, nombre del archivo y la URL."))
        
        file_content = base64.b64decode(self.file)

        files = {
            'file': (self.file_name, file_content)
        }

        try:
            response = requests.post(self.url, files=files)

            response.raise_for_status() 
            result=response.json()
        

            partner=self.env['res.partner'].search([
                ('name','=',result['Empresa']['Nombre'])
            ],limit=1)

            picking_type=self.env.ref('stock.picking_type_in')

            moves_items=[]

            for item in result['Productos']:
                product=self.env['product.product'].search([
                    ('name','=',item['Descripcion'])
                    ],limit=1)
                
                if product:
                    moves_items.append((0,0,{
                        'name':product.name,
                        'product_id':product.id,
                        'product_uom':product.uom_id.id,
                        'product_uom_qty':float(item['Cantidad']),
                        'location_id':picking_type.default_location_src_id.id,
                        'location_dest_id':picking_type.default_location_dest_id.id
                    }))

            # return {
            #     'type': 'ir.actions.client',
            #     'tag': 'display_notification',
            #     'params': {
            #         'title': _('Archivo enviado'),
            #         'message': _(f'Total de items procesados : {str(total_items)} items.'),
            #         'type': 'success',
            #         'sticky': False,
            #     }
            # }

            
            return {
            'type': 'ir.actions.act_window',
            'name': 'Recepción de Inventario',
            'res_model': 'stock.picking',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_partner_id': partner.id,
                'default_picking_type_id': picking_type.id,
                'default_origin': result['Factura']['Numero'],
                'default_scheduled_date': fields.Datetime.now(),
                'default_move_ids_without_package': moves_items
            }
            }

        except Exception as e:
            print("Error:", str(e))
            raise UserError(_("Error al enviar el archivo: %s") % str(e))
