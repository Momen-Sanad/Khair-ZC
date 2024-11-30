from flask import Blueprint, request, jsonify, redirect, url_for, session
from models.dbSchema import db, Charity


# Create an API endpoint that allows admins to edit (create, update, delete) campaigns.
# Admins should be able to control event visibility, details, and capacity.
# Acceptance criteria:
# Endpoint allows admins to create, update, and delete campaigns.
# Admins can manage which charities are linked to specific campaigns.
# Priority: Medium-High

manage_campaign_bp = Blueprint('manage_campaign', __name__)


# route is /manage_campaign/create
# @search_bp.route('/create', methods=['POST'])
# def create_campaign():
