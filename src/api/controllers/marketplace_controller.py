from flask import Blueprint, request, jsonify
from services.marketplace_service import MarketplaceService

bp = Blueprint('marketplace', __name__, url_prefix='/api/v1/marketplace')
service = MarketplaceService()

@bp.route('/products', methods=['GET'])
def get_products():
    """
    Get list of products
    ---
    get:
      summary: Retrieve all marketplace products
      tags:
        - Marketplace
      parameters:
        - name: category
          in: query
          required: false
          schema:
            type: string
          description: Filter products by category
      responses:
        '200':
          description: List of products retrieved successfully
    """
    category = request.args.get('category')
    products = service.list_products(category)
    return jsonify(products), 200

@bp.route('/products', methods=['POST'])
def create_product():
    """
    Create a new product listing
    ---
    post:
      summary: Create a new product
      tags:
        - Marketplace
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                seller_id:
                  type: integer
                title:
                  type: string
                description:
                  type: string
                price:
                  type: number
                category:
                  type: string
      responses:
        '201':
          description: Product created successfully
    """
    data = request.get_json() or {}
    seller_id = data.get('seller_id', 1)
    product = service.add_product(seller_id, data)
    return jsonify(product), 201