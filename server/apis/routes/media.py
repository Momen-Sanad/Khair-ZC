from flask import Blueprint, request, jsonify, redirect, url_for, session
from models.dbSchema import db, Media
from datetime import datetime

media_bp = Blueprint('media', __name__)

@media_bp.route('/images', methods=['GET'])
def get_images():
    images = Media.query.all()
    json_images = []
    if images:
        json_images = [
            {
                "id": image.id,
                "url": image.image_link
            }
            for image in images
        ]
    else:
        return jsonify({"message": "No images available."}), 404

    return jsonify(json_images), 200
