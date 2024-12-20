from flask import Blueprint, request, jsonify, redirect, url_for, session
from models.dbSchema import db, Merch
from datetime import datetime


shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/products',methods=['GET'])
def get_products():  
    products = Merch.query.all()
    json_products = []
    if products:
        json_products = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "image":product.image
        }
        for product in products]
    return jsonify(json_products), 200