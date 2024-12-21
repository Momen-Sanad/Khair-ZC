from flask import Blueprint, request, jsonify
from models.dbSchema import db, Merch
from datetime import datetime
from apis.routes.Security import session_required, admin_required
from models.Notifications import ErrorProcessor

shop_bp = Blueprint('shop', __name__)
error_processor = ErrorProcessor()

@shop_bp.route('/products', methods=['GET'])
def get_products():
    products = Merch.query.all()
    json_products = []

    # Check if any products exist
    if products:
        json_products = [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "image": product.image
            }
            for product in products
        ]
    else:
        return error_processor.process_error("shop_no_products"), 404

    return jsonify(json_products), 200


@shop_bp.route('/products/add', methods=['POST'])
@session_required
@admin_required
def add_products():
    try:
        # Parse JSON request
        product_data = request.json

        # Extract required fields
        name = product_data.get('name')
        description = product_data.get('description')
        price = product_data.get('price')
        image = product_data.get('image')

        # Validate fields
        if not all([name, description, price, image]):
            return error_processor.process_error("shop_missing_fields"), 400

        if not isinstance(price, (int, float)) or price <= 0:
            return error_processor.process_error("shop_invalid_price"), 400

        # Check if product already exists
        existing_product = Merch.query.filter_by(name=name).first()
        if existing_product:
            return error_processor.process_error("shop_duplicate_product"), 400

        # Add new product
        new_product = Merch(
            name=name,
            description=description,
            price=price,
            image=image
        )
        db.session.add(new_product)
        db.session.commit()

        return error_processor.process_error("shop_product_added"), 201

    except Exception as e:
        db.session.rollback()
        return error_processor.process_error("shop_add_product_error"), 500
