from flask import Blueprint, jsonify, request

from services.transaction_fee_service import TransactionFeeService
from api.middleware import token_required, role_required


bp = Blueprint(
    'transaction_fee',
    __name__,
    url_prefix='/transaction-fees'
)

transaction_fee_service = TransactionFeeService()


@bp.route('/', methods=['GET'])
@token_required
@role_required('admin')
def get_all_fees():
    fees = transaction_fee_service.list_all()

    result = []

    for fee in fees:
        result.append({
            'id': str(fee.id),
            'transaction_id': str(fee.transaction_id),
            'fee_amount': fee.fee_amount
        })

    return jsonify(result), 200


@bp.route('/', methods=['POST'])
@token_required
@role_required('admin')
def create_fee():
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Invalid request'
        }), 400

    if not data.get('transaction_id'):
        return jsonify({
            'message': 'transaction_id is required'
        }), 400

    if data.get('fee_amount') is None:
        return jsonify({
            'message': 'fee_amount is required'
        }), 400

    fee = transaction_fee_service.create(data)

    return jsonify({
        'message': 'Transaction fee created successfully',
        'fee': {
            'id': str(fee.id),
            'transaction_id': str(fee.transaction_id),
            'fee_amount': fee.fee_amount
        }
    }), 201


@bp.route('/<uuid:fee_id>', methods=['GET'])
@token_required
@role_required('admin')
def get_fee(fee_id):
    fee = transaction_fee_service.get_by_id(fee_id)

    if not fee:
        return jsonify({
            'message': 'Transaction fee not found'
        }), 404

    return jsonify({
        'id': str(fee.id),
        'transaction_id': str(fee.transaction_id),
        'fee_amount': fee.fee_amount
    }), 200


@bp.route('/<uuid:fee_id>', methods=['PUT'])
@token_required
@role_required('admin')
def update_fee(fee_id):
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Invalid request'
        }), 400

    fee = transaction_fee_service.update(
        fee_id=fee_id,
        data=data
    )

    if not fee:
        return jsonify({
            'message': 'Transaction fee not found'
        }), 404

    return jsonify({
        'message': 'Transaction fee updated successfully',
        'fee': {
            'id': str(fee.id),
            'transaction_id': str(fee.transaction_id),
            'fee_amount': fee.fee_amount
        }
    }), 200


@bp.route('/<uuid:fee_id>', methods=['DELETE'])
@token_required
@role_required('admin')
def delete_fee(fee_id):
    deleted = transaction_fee_service.delete(fee_id)

    if not deleted:
        return jsonify({
            'message': 'Transaction fee not found'
        }), 404

    return jsonify({
        'message': 'Transaction fee deleted successfully'
    }), 200