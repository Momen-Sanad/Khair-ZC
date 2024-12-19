import datetime
from flask import Blueprint, request, jsonify
from models.dbSchema import db, Charity
from Security import session_required, admin_required
from error_processor import ErrorProcessor

charity_bp = Blueprint('charity', __name__)
error_processor = ErrorProcessor()

@charity_bp.route('/create', methods=['POST'])
@session_required
@admin_required
def create():
    from models.dbSchema import User

    charities = request.json  # Expecting a list of charities in the request body

    if not charities or not isinstance(charities, list):
        return jsonify(error_processor.process_error("charity_invalid_input")), 400

    created_charities = []
    for charity_data in charities:
        charity_id = charity_data.get('charId')
        charity_name = charity_data.get('charName')
        charity_address = charity_data.get('charAdd')
        charity_desc = charity_data.get('charDesc')
        charity_cat = charity_data.get('charCat')

        # Validate required fields
        if not all([charity_name, charity_address, charity_desc, charity_cat]):
            return jsonify(error_processor.process_error("charity_missing_fields")), 400

        # Check if charity already exists
        existing_charity = Charity.query.filter_by(name=charity_name).first()
        if existing_charity:
            return jsonify(error_processor.process_error("charity_exists", name=charity_name)), 400

        # Create new charity
        new_charity = Charity(
            id=charity_id,
            name=charity_name,
            address=charity_address,
            description=charity_desc,
            category=charity_cat
        )

        db.session.add(new_charity)
        created_charities.append({"charityId": charity_id, "charityName": charity_name})

    db.session.commit()
    return jsonify({"message": "Charities created successfully", "charities": created_charities}), 201
