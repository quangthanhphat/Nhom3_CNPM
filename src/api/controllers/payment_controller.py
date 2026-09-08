from flask import Blueprint, jsonify, request

from services.payment_service import PaymentService
from api.middleware import token_required, role_required


bp = Blueprint(
    'payment',
    __name__,
    url_prefix='/payments'
)

payment_service = PaymentService()


# =========================
# GET ALL PAYMENTS
# =========================

@bp.route('/', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'admin'
)
def get_all_payments():
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    payments = payment_service.list_for_user(
        user_id=user_id,
        role=role
    )

    result = []

    for payment in payments:
        result.append({
            'id': str(payment.id),
            'order_id': str(payment.order_id),
            'amount': payment.amount,
            'transaction_reference': payment.transaction_reference,
            'status': payment.status,
            'paid_at': payment.paid_at
        })

    return jsonify(result), 200


# =========================
# CREATE PAYMENT
# =========================

@bp.route('/', methods=['POST'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'admin'
)
def create_payment():
    data = request.get_json()

    user_id = request.user.get('user_id')
    role = request.user.get('role')

    payment, error = payment_service.create(
        data=data,
        user_id=user_id,
        role=role
    )

    if error == 'order_not_found':
        return jsonify({
            'message': 'Order not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to create payment for this order'
            )
        }), 403

    return jsonify({
        'message': 'Payment created successfully',
        'payment': {
            'id': str(payment.id),
            'order_id': str(payment.order_id),
            'amount': payment.amount,
            'transaction_reference': payment.transaction_reference,
            'status': payment.status,
            'paid_at': payment.paid_at
        }
    }), 201


# =========================
# GET PAYMENT BY ID
# =========================

@bp.route('/<uuid:payment_id>', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'admin'
)
def get_payment(payment_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    payment, error = payment_service.get_by_id_for_user(
        payment_id=payment_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Payment not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to view this payment'
            )
        }), 403

    return jsonify({
        'id': str(payment.id),
        'order_id': str(payment.order_id),
        'amount': payment.amount,
        'transaction_reference': payment.transaction_reference,
        'status': payment.status,
        'paid_at': payment.paid_at
    }), 200


# =========================
# UPDATE PAYMENT
# =========================

@bp.route('/<uuid:payment_id>', methods=['PUT'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'admin'
)
def update_payment(payment_id):
    data = request.get_json()

    user_id = request.user.get('user_id')
    role = request.user.get('role')

    payment, error = payment_service.update(
        payment_id=payment_id,
        data=data,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Payment not found'
        }), 404

    if error == 'order_not_found':
        return jsonify({
            'message': 'Order not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to update this payment'
            )
        }), 403

    return jsonify({
        'message': 'Payment updated successfully',
        'payment': {
            'id': str(payment.id),
            'order_id': str(payment.order_id),
            'amount': payment.amount,
            'transaction_reference': payment.transaction_reference,
            'status': payment.status,
            'paid_at': payment.paid_at
        }
    }), 200


# =========================
# DELETE PAYMENT
# =========================

@bp.route('/<uuid:payment_id>', methods=['DELETE'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'admin'
)
def delete_payment(payment_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    deleted, error = payment_service.delete(
        payment_id=payment_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Payment not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to delete this payment'
            )
        }), 403

    return jsonify({
        'message': 'Payment deleted successfully'
    }), 200