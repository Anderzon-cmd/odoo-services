# -*- coding: utf-8 -*-
# from odoo import http


import json

import requests
from odoo.http import Response, request
from odoo import http


class InventoryServices(http.Controller):
    @http.route('/module/inventory-services/sales', auth='public', type='http', methods=['GET'])
    def sales(self, **kw):
        try:
            sales_orders = request.env['sale.order'].sudo().search([])
            sales_data = []

            for order in sales_orders:
                sales_data.append({
                    'id': order.id,
                    'name': order.name,
                    'partner': order.partner_id.name if order.partner_id else None,
                    'date_order': order.date_order.isoformat() if order.date_order else None,
                    'amount_total': order.amount_total,
                    'state': order.state,
                })

            return Response(
            json.dumps({'data': sales_data, 'message': 'Sales orders retrieved successfully'}),
            status=200,
            content_type='application/json'
            )
        except Exception as e:
            print(str(e),'error')
            return Response(
            json.dumps({'data': None, 'message': 'Error retrieving sales orders'}),
            status=500,
            content_type='application/json'
            )
    
    @http.route('/module/inventory-services/product/<int:product_id>', auth='public', type='http', methods=['GET'])
    def product(self, product_id, **kw):
        try:
            product = request.env['product.template'].sudo().search([('id', '=', product_id)])

            if not product.exists():
                return Response(
                    json.dumps({'data': None, 'message': 'Item not found'}),
                    status=404,
                    content_type='application/json'
                )
            return Response(
                json.dumps({
                    'data': {
                        'id': product.id,
                        'name': product.name,
                        'default_code': product.default_code,
                        'description': product.description_sale,
                        'list_price': product.list_price,
                        'assets_names':json.loads(product.asset_id.assets_names) if product.asset_id else [],
                    },
                    'message': 'Product retrieved successfully'
                }),
                status=200,
                content_type='application/json'
            )
        except Exception as e:
            print(str(e), 'error')
            return Response(
                json.dumps({'data': None, 'message': 'Error retrieving product'}),
                status=500,
                content_type='application/json'
            )
        
    @http.route('/module/inventory-services/test', auth='public', type='http', methods=['GET'])  
    def testing(self, **kw):
        url="https://d130-161-56-10-65.ngrok-free.app/extract"
        try:
            response = requests.get(url, timeout=10)
            print(response.status_code)
            if response.status_code == 200:
                data = response.json()
                
                return Response(
                    json.dumps({'data': data, 'message': 'Data retrieved successfully'}),
                    status=200,
                    content_type='application/json'
                )
            else:
                return Response(
                    json.dumps({'data': None, 'message': 'Error retrieving data'}),
                    status=500,
                    content_type='application/json'
                )
        except Exception as e:
            print(str(e), 'error')
            return Response(
                json.dumps({'data': None, 'message': 'Error retrieving data'}),
                status=500,
                content_type='application/json'
            )
            

    

