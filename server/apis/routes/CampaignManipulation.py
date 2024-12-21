import datetime
from flask import Blueprint, request, jsonify, redirect, url_for, session
from requests_oauthlib import OAuth2Session
import oauthlib
import oauth
from flask_bcrypt import Bcrypt
import regex
from functools import wraps
import cryptography
import jwt
from authlib.integrations.flask_client import OAuth
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from requests_oauthlib import OAuth2Session
from models.dbSchema import db, Campaign, Charity
from models.Notifications import ErrorProcessor
from apis.routes.Security import session_required, admin_required

campaign_bp = Blueprint('Campaign', __name__)
Notifications = ErrorProcessor()


@campaign_bp.route('/create', methods=['POST'])
@session_required
@admin_required
def create():
    from models.dbSchema import User, db, Campaign

    campaigns = request.json  # Expecting a list of campaigns in the request body

    if not campaigns or not isinstance(campaigns, list):
        return jsonify(Notifications.process_error("search_invalid")), 400

    created_campaigns = []

    for campaign_data in campaigns:
        # Extract campaign data
        user_id = campaign_data.get('userId')
        campaign_id = campaign_data.get('campaignId')
        campaign_name = campaign_data.get('campaignName')
        campaign_reward = campaign_data.get('campaignRe')
        campaign_desc = campaign_data.get('campaignDesc')
        campaign_date = campaign_data.get('campaignDate')
        campaign_cap = campaign_data.get('campaignCap')
        connected_charity = campaign_data.get('charId')

        # Validate required fields
        if not all([campaign_name, campaign_reward, campaign_desc, campaign_cap, connected_charity]):
            return jsonify(Notifications.process_error("admin_campaign_create")), 400

        # Check if campaign already exists
        existing_campaign = Campaign.query.filter_by(
            title=campaign_name).first()
        if existing_campaign:
            return jsonify(Notifications.process_error("campaign_follow")), 400

        existing_campaign = Campaign.query.filter_by(id=campaign_id).first()
        if existing_campaign:
            return jsonify(Notifications.process_error("campaign_follow")), 400

        # Check if charity exists
        if not Charity.query.filter_by(id=connected_charity).first():
            return jsonify(Notifications.process_error("charity_unregister")), 400

        # Create new campaign
        new_campaign = Campaign(
            id=campaign_id,
            title=campaign_name,
            reward=campaign_reward,
            description=campaign_desc,
            charity_id=connected_charity,
            date=campaign_date,
            capacity=campaign_cap
        )

        db.session.add(new_campaign)
        created_campaigns.append(
            {"campaignId": campaign_id, "campaignName": campaign_name})

    db.session.commit()
    return jsonify(Notifications.process_error("admin_campaign_create")), 201


@campaign_bp.route('/campaigns', methods=['GET'])
def get_campaigns():
    # Fetch all campaigns from the database
    campaigns = Campaign.query.all()

    # Serialize the campaigns to JSON
    campaigns_data = [
        {
            "id": campaign.id,
            "title": campaign.title,
            "description": campaign.description,
            "day": campaign.date.day,
            "month": campaign.date.strftime('%B').upper(), 
            "author": campaign.user.fname + " " + campaign.user.lname if campaign.user else "Unknown", 
            "time": "Posted " + str((datetime.utcnow() - campaign.date).days) + " days ago"
        }
        for campaign in campaigns
    ]

    return jsonify({"campaigns": campaigns_data}), 200

@campaign_bp.route('/update', methods=['PUT'])
@session_required
@admin_required
def update():
    from models.dbSchema import db, Campaign

    campaign = request.json
    campaign_id = campaign.get('campaignId')
    campaign_name = campaign.get('campaignName')
    campaign_reward = campaign.get('campaignRe')
    campaign_desc = campaign.get('campaignDesc')
    campaign_date = campaign.get('campaignDate')
    campaign_cap = campaign.get('campaignCap')
    connected_charity = campaign.get('charId')

    if not campaign_id:
        return jsonify(Notifications.process_error("campaign_unregister")), 400

    existing_campaign = Campaign.query.filter_by(id=campaign_id).first()
    if not existing_campaign:
        return jsonify(Notifications.process_error("campaign_not_attended")), 404

    if campaign_name:
        existing_campaign.title = campaign_name

    if campaign_reward:
        existing_campaign.reward = campaign_reward

    if campaign_desc:
        existing_campaign.description = campaign_desc

    if campaign_date:
        existing_campaign.date = campaign_date

    if campaign_cap:
        existing_campaign.capacity = campaign_cap

    if connected_charity:
        if not Charity.query.filter_by(id=connected_charity).first():
            return jsonify(Notifications.process_error("charity_unregister")), 404
        existing_campaign.charity_id = connected_charity

    db.session.commit()
    return jsonify(Notifications.process_error("admin_campaign_update")), 200


@campaign_bp.route('/delete', methods=['DELETE'])
@session_required
@admin_required
def delete():
    from models.dbSchema import Campaign

    campaign_id = request.json.get('campaignId')

    if not campaign_id or not isinstance(campaign_id, int):
        return jsonify(Notifications.process_error("campaign_unregister")), 400

    # if the campaign does not exist, return 404
    if not Campaign.query.filter_by(id=campaign_id).first():
        return jsonify(Notifications.process_error("campaign_not_attended")), 404

    existing_campaign = Campaign.query.filter_by(id=campaign_id).first()

    if not existing_campaign:
        return jsonify(Notifications.process_error("campaign_not_attended")), 404

    db.session.delete(existing_campaign)
    db.session.commit()
    return jsonify(Notifications.process_error("admin_campaign_delete")), 200
