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
                    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

                    body {{
                        font-family: 'Inter', sans-serif;
                        color: #1f2937;
                        background-color: #f9fafb;
                        margin: 0;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background: linear-gradient(145deg, #ffffff, #f3f4f6);
                        padding: 32px;
                        border-radius: 12px;
                        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                    }}
                    h1 {{
                        color: #4f46e5;
                        font-size: 28px;
                        font-weight: 700;
                        margin-bottom: 24px;
                    }}
                    p {{
                        font-size: 16px;
                        line-height: 1.6;
                        margin-bottom: 16px;
                    }}
                    .highlight {{
                        background-color: #e0e7ff;
                        color: #4338ca;
                        padding: 12px;
                        border-radius: 8px;
                        font-weight: 600;
                    }}
                    .cta {{
                        background-color: #4f46e5;
                        color: #ffffff;
                        padding: 12px 24px;
                        border-radius: 6px;
                        text-decoration: none;
                        display: inline-block;
                        font-weight: 600;
                        margin-top: 24px;
                    }}
                    .footer {{
                        margin-top: 32px;
                        font-size: 14px;
                        color: #6b7280;
                        border-top: 1px solid #e5e7eb;
                        padding-top: 16px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Safe Journey Notification</h1>
                    <p>Dear {contact.name},</p>
                    <p>We hope this message finds you well. We wanted to inform you that <strong>{user.fullname}</strong> has safely checked out and begun their journey.</p>
                    <p class="highlight">Important Note: {note}</p>
                    <p>At SafeReturn, we prioritize the well-being of all our users. While {user.fullname} is away, we'll be monitoring their status and will keep you updated on any significant changes.</p>
                    <p>We understand the importance of peace of mind when loved ones are traveling. Rest assured, our team is committed to ensuring a safe and smooth experience for everyone involved.</p>
                    <a href="#" class="cta">View Journey Details</a>
                    <p>If you have any questions or concerns, please don't hesitate to reach out to our support team. We're here to help 24/7.</p>
                    <div class="footer">
                        Wishing {user.fullname} a safe return,<br>
                        Your dedicated SafeReturn Team
                    </div>
                </div>
            </body>
            </html>
            """
            send_email(contact.email, 'Safe Journey Notification', email_body)

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
