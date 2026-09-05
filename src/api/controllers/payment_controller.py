from flask import Blueprint, jsonify, request

from services.payment_service import PaymentService
from api.middleware import token_required


bp = Blueprint(
    'payment',
    __name__,
    url_prefix='/payments'
)

payment_service = PaymentService()


@bp.route('/', methods=['GET'])
@token_required
def get_all_payments():
    payments = payment_service.list_all()

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


@bp.route('/', methods=['POST'])
@token_required
def create_payment():
    data = request.get_json()

    payment = payment_service.create(data)

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


@bp.route('/<uuid:payment_id>', methods=['GET'])
@token_required
def get_payment(payment_id):
    payment = payment_service.get_by_id(payment_id)

    if not payment:
        return jsonify({
            'message': 'Payment not found'
        }), 404

    return jsonify({
        'id': str(payment.id),
        'order_id': str(payment.order_id),
        'amount': payment.amount,
        'transaction_reference': payment.transaction_reference,
        'status': payment.status,
        'paid_at': payment.paid_at
    }), 200


@bp.route('/<uuid:payment_id>', methods=['PUT'])
@token_required
def update_payment(payment_id):
    data = request.get_json()

    payment = payment_service.update(
        payment_id=payment_id,
        data=data
    )

    if not payment:
        return jsonify({
            'message': 'Payment not found'
        }), 404

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


@bp.route('/<uuid:payment_id>', methods=['DELETE'])
@token_required
def delete_payment(payment_id):
    deleted = payment_service.delete(payment_id)

    if not deleted:
        return jsonify({
            'message': 'Payment not found'
        }), 404

    return jsonify({
        'message': 'Payment deleted successfully'
    }), 200