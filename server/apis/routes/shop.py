from flask import Blueprint, request, jsonify, redirect, url_for, session
from models.dbSchema import db, Merch
from datetime import datetime

shop_bp = Blueprint('shop', __name__)

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
        return jsonify({"message": "No products available."}), 404

    return jsonify(json_products), 200


@shop_bp.route('/products/add', methods=['POST'])
def add_products():
    try:
        product_data = request.json

        # field extraction
        name =        product_data.get('name')
        description = product_data.get('description')
        price =       product_data.get('price')
        image =       product_data.get('image')

        # validate fields
        if not all([name, description, price, image]):
            return jsonify({"error": "All fields (name, description, price, image) are required."}), 400

        if not isinstance(price, (int, float)) or price <= 0:
            return jsonify({"error": "Price must be a positive number."}), 400

        # check if product already exists
        existing_product = Merch.query.filter_by(name=name).first()
        if existing_product:
            return jsonify({"error": f"Product '{name}' already exists."}), 400

        # add product
        new_product = Merch(
            name=name,
            description=description,
            price=price,
            image=image
        )
        db.session.add(new_product)
        db.session.commit()

        return jsonify({"message": "Product added successfully.", "product": {
            "id":          new_product.id,
            "name":        new_product.name,
            "description": new_product.description,
            "price":       new_product.price,
            "image":       new_product.image
        }}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while adding the product.", "details": str(e)}), 500
