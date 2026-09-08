from flask import Blueprint, jsonify, request

from services.processing_workflow_service import ProcessingWorkflowService
from api.middleware import token_required, role_required


bp = Blueprint(
    'processing_workflow',
    __name__,
    url_prefix='/processing-workflows'
)

processing_workflow_service = ProcessingWorkflowService()


# =========================
# GET ALL WORKFLOWS
# =========================

@bp.route('/', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'admin'
)
def get_all_workflows():
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    workflows = processing_workflow_service.list_for_user(
        user_id=user_id,
        role=role
    )

    result = []

    for workflow in workflows:
        result.append({
            'id': str(workflow.id),
            'order_id': str(workflow.order_id),
            'stage': workflow.stage,
            'status': workflow.status,
            'started_at': workflow.started_at,
            'completed_at': workflow.completed_at,
            'notes': workflow.notes
        })

    return jsonify(result), 200


# =========================
# CREATE WORKFLOW
# =========================

@bp.route('/', methods=['POST'])
@token_required
@role_required(
    'film_lab_owner',
    'admin'
)
def create_workflow():
    data = request.get_json()

    user_id = request.user.get('user_id')
    role = request.user.get('role')

    workflow, error = processing_workflow_service.create(
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
                'You can only create workflows '
                'for orders of your own film lab'
            )
        }), 403

    return jsonify({
        'message': 'Processing workflow created successfully',
        'workflow': {
            'id': str(workflow.id),
            'order_id': str(workflow.order_id),
            'stage': workflow.stage,
            'status': workflow.status,
            'started_at': workflow.started_at,
            'completed_at': workflow.completed_at,
            'notes': workflow.notes
        }
    }), 201


# =========================
# GET WORKFLOW BY ID
# =========================

@bp.route('/<uuid:workflow_id>', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'admin'
)
def get_workflow(workflow_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    workflow, error = processing_workflow_service.get_by_id_for_user(
        workflow_id=workflow_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Processing workflow not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to view this workflow'
            )
        }), 403

    return jsonify({
        'id': str(workflow.id),
        'order_id': str(workflow.order_id),
        'stage': workflow.stage,
        'status': workflow.status,
        'started_at': workflow.started_at,
        'completed_at': workflow.completed_at,
        'notes': workflow.notes
    }), 200


# =========================
# UPDATE WORKFLOW
# =========================

@bp.route('/<uuid:workflow_id>', methods=['PUT'])
@token_required
@role_required(
    'film_lab_owner',
    'admin'
)
def update_workflow(workflow_id):
    data = request.get_json()

    user_id = request.user.get('user_id')
    role = request.user.get('role')

    workflow, error = processing_workflow_service.update(
        workflow_id=workflow_id,
        data=data,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Processing workflow not found'
        }), 404

    if error == 'order_not_found':
        return jsonify({
            'message': 'Order not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to update this workflow'
            )
        }), 403

    return jsonify({
        'message': 'Processing workflow updated successfully',
        'workflow': {
            'id': str(workflow.id),
            'order_id': str(workflow.order_id),
            'stage': workflow.stage,
            'status': workflow.status,
            'started_at': workflow.started_at,
            'completed_at': workflow.completed_at,
            'notes': workflow.notes
        }
    }), 200


# =========================
# DELETE WORKFLOW
# =========================

@bp.route('/<uuid:workflow_id>', methods=['DELETE'])
@token_required
@role_required(
    'film_lab_owner',
    'admin'
)
def delete_workflow(workflow_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    deleted, error = processing_workflow_service.delete(
        workflow_id=workflow_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Processing workflow not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to delete this workflow'
            )
        }), 403

    return jsonify({
        'message': 'Processing workflow deleted successfully'
    }), 200