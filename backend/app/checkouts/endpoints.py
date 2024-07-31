from flask import Blueprint, jsonify, request
from app.models import db
from app.models.Checkout import Checkout
from app.models.Users import User
from app.models.Contacts import EmergencyContact
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.utils import send_email 

checkout_bp = Blueprint("checkout", __name__, url_prefix="/checkouts")

@checkout_bp.post('/create')
@jwt_required()
def create_checkout():
    """
    @Description:
        Records a user checking out and notifies their emergency contacts
    """
    try:
        data = request.json
        note = data.get('note')
        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user).first()
        if not user:
            return jsonify(error="User not found"), 401
        
        # Check if user has a pending checkout 
        active_checkout = Checkout.query.filter(
            Checkout.user_id == user.id,
            Checkout.is_returned == False # noqa
        ).first()
        if active_checkout:
            return jsonify(error="You have a pending checkout. Close it to create a new checkout!"), 403
        
        # Create new checkout record
        new_checkout = Checkout(
            note=note,
            user_id=current_user
        )
        db.session.add(new_checkout)
        db.session.commit()
        
        # Fetch emergency contacts
        contacts = EmergencyContact.query.filter_by(user_id=current_user).all()

        # Send email to each contact
        for contact in contacts:
            email_body = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        color: #333;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: #fff;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }}
                    h1 {{
                        color: #007bff;
                        font-size: 24px;
                    }}
                    p {{
                        font-size: 16px;
                        line-height: 1.6;
                    }}
                    .footer {{
                        margin-top: 20px;
                        font-size: 14px;
                        color: #777;
                    }}
                    .highlight {{
                        background-color: #e9ecef;
                        padding: 10px;
                        border-radius: 4px;
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Checkout Notification</h1>
                    <p>Dear {contact.name},</p>
                    <p><strong>{user.fullname}</strong> has checked out.</p>
                    <p><span class="highlight">Note:</span> {note}</p>
                    <p>We hope they return safely. Thank you for your attention!</p>
                    <div class="footer">
                        Best regards,<br>Your SafeReturn Team
                    </div>
                </div>
            </body>
            </html>
            """
            send_email(contact.email, 'Checkout Notification', email_body)

        return jsonify(message="Checkout created successfully and contacts have been notified! Get back safe!"), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify(error=f"We are really sorry about this! {e}")

# Get all user checkouts endpoint 
@checkout_bp.get('/all')
@jwt_required()
def get_user_checkouts():
    """
    @Description:
        Get all checkouts for the current user
    """
    try:
        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user).first()
        if not user:
            return jsonify(error="User not found"), 403
        
        checkouts = Checkout.query.filter_by(user_id=current_user).all()
        return jsonify(checkouts=[{
            'id': checkout.id,
            'checkout_time': checkout.checkout_time,
            'note': checkout.note,
            'is_returned': checkout.is_returned,
            'return_time': checkout.return_time
        } for checkout in checkouts]), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(error=f"We are really sorry about this! {e}")

 
@checkout_bp.put('/<checkout_id>/update')
@jwt_required()
def update_user_checkout(checkout_id: int):
    """
    @Description:
        Update user's checkout. This endpoint will set is_returned to true and set the return time.
    """
    try:
        current_user = get_jwt_identity()
        checkout = Checkout.query.filter_by(id=checkout_id, user_id=current_user).first()
        
        if not checkout:
            return jsonify(error="Checkout not found"), 404
        
        if checkout.is_returned:
            return jsonify(error="Checkout already marked as returned"), 403

        checkout.is_returned = True
        checkout.return_time = datetime.now()
        db.session.commit()
        
        return jsonify(message="Checkout updated successfully!"), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify(error=f"We are really sorry about this! {e}")
 
@checkout_bp.get('/<checkout_id>/details')
@jwt_required()
def get_user_checkout_details(checkout_id: int):
    """
    @Description:
        Retrieve details of a specific checkout.
    """
    try:
        current_user = get_jwt_identity()
        checkout = Checkout.query.filter_by(id=checkout_id, user_id=current_user).first()
        
        if not checkout:
            return jsonify(error="Checkout not found"), 404

        return jsonify({
            'id': checkout.id,
            'checkout_time': checkout.checkout_time,
            'note': checkout.note,
            'is_returned': checkout.is_returned,
            'return_time': checkout.return_time
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify(error=f"We are really sorry about this! {e}")
