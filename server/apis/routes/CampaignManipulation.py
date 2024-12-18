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

campaign_bp = Blueprint('Campaign', __name__)


@campaign_bp.route('/create', methods=['POST'])
def create():
    from models.dbSchema import User,db,Campaign
    
    campaigns = request.json  # Expecting a list of campaigns in the request body

    if not campaigns or not isinstance(campaigns, list):
        return jsonify({"error": "Invalid input, expected a list of campaigns"}), 400

    created_campaigns = []
        
    for campaign_data in campaigns:
        #sql query "join"
        user_id = campaign_data.get('userId')
        campaign_id = campaign_data.get('campaignId')
        campaign_name = campaign_data.get('campaignName')
        campaign_reward = campaign_data.get('campaignRe')
        campaign_desc = campaign_data.get('campaignDesc')
        campaign_date = campaign_data.get('campaignDate')
        campaign_cap = campaign_data.get('campaignCap')
        connected_charity = campaign_data.get('charId')
        #O(1)
        #O(N)
        # check if user is admin
        user = User.query.filter_by(id=user_id).first()
        if not user or not user.is_admin:
            return jsonify({"error": "Only admins can create campaigns"}), 403

        # Validate required fields
        if not all([campaign_name, campaign_reward, campaign_desc, campaign_cap, connected_charity]):
            return jsonify({"error": "Missing required fields for one or more campaigns"}), 400

        # Check if campaign already exists
        existing_campaign = Campaign.query.filter_by(title=campaign_name).first()
        if existing_campaign:
            return jsonify({"error": f"campaign '{campaign_name}' already exists"}), 400

        # Check if charity exists
        if not Charity.query.filter_by(id=connected_charity).first():
            return jsonify({"error": f"Charity ID {connected_charity} not found"}), 400

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
        created_campaigns.append({"campaignId": campaign_id, "campaignName": campaign_name})

    db.session.commit()
    return jsonify({"message": "campaigns created successfully", "campaigns": created_campaigns}), 201


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
def update():
    from models.dbSchema import User,db
    
    campaign = request.json
    campaign_id = campaign.get('campaignId')
    campaign_name = campaign.get('campaignName')
    campaign_reward = campaign.get('campaignRe')
    campaign_desc = campaign.get('campaignDesc')
    campaign_date = campaign.get('campaignDate')
    campaign_cap = campaign.get('campaignCap')
    connected_charity = campaign.get('charId')
    user_id = campaign.get('is_admin')


    user = User.query.filter_by(id=user_id).first()
    if not user or not user.is_admin:
        return jsonify({"error": "Only admins can update campaigns"}), 403

    if not campaign_id:
        return jsonify({"error": "campaign ID is required"}), 400

    existing_campaign = campaign.query.filter_by(id=campaign_id).first()
    if not existing_campaign:
        return jsonify({"error": "campaign not found"}), 404

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
            return jsonify({"error": "Charity not found"}), 404
        existing_campaign.charity_id = connected_charity

    db.session.commit()
    return jsonify({"message": "campaign updated successfully"}), 200


# delete campaign

@campaign_bp.route('/delete', methods=['DELETE'])
def delete():
    from models.dbSchema import User,Campaign
    user_id = request.json.get('userId')
    campaign_id = request.json.get('campaignId')
    

    user = User.query.filter_by(id=user_id).first()
    if not user or not user.is_admin:
        return jsonify({"error": "Only admins can delete campaigns"}), 403
    
    if not campaign_id:
        return jsonify({"error": "campaign ID is required"}), 400   

    existing_campaign = Campaign.query.filter_by(id=campaign_id).first()

    if not existing_campaign:
        return jsonify({"error": "campaign not found"}), 404

    db.session.delete(existing_campaign)
    db.session.commit()
    return jsonify({"message": "campaign deleted successfully"}), 200