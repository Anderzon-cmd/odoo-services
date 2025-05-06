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

    url=fields.Char(string="URL", required=True, help="Endpoint URL to send the file")


    def action_import_file(self):
        print("URL:", self.url)
        print("File:", self.file)
        if not self.file or not self.url:
            raise UserError(_("Debe proporcionar el archivo, nombre del archivo y la URL."))
        
        file_content = base64.b64decode(self.file)

        files = {
            'file': ('invoice.pdf', file_content)
        }

        try:
            response = requests.post(self.url, files=files)

            response.raise_for_status() 
            result=response.json()
            
            print(result)
            

            total_items=len(result['Productos'])
            
            print(total_items)
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Archivo enviado'),
                    'message': _(f'Total de items procesados : {str(total_items)} items.'),
                    'type': 'success',
                    'sticky': False,
                }
            }

        except Exception as e:
            print("Error:", str(e))
            raise UserError(_("Error al enviar el archivo: %s") % str(e))
