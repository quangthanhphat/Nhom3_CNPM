from flask import Blueprint, jsonify, request

from services.processing_workflow_service import ProcessingWorkflowService
from api.middleware import token_required


bp = Blueprint(
    'processing_workflow',
    __name__,
    url_prefix='/processing-workflows'
)

processing_workflow_service = ProcessingWorkflowService()


@bp.route('/', methods=['GET'])
@token_required
def get_all_workflows():
    workflows = processing_workflow_service.list_all()

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


@bp.route('/', methods=['POST'])
@token_required
def create_workflow():
    data = request.get_json()

    workflow = processing_workflow_service.create(data)

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


@bp.route('/<uuid:workflow_id>', methods=['GET'])
@token_required
def get_workflow(workflow_id):
    workflow = processing_workflow_service.get_by_id(workflow_id)

    if not workflow:
        return jsonify({
            'message': 'Processing workflow not found'
        }), 404

    return jsonify({
        'id': str(workflow.id),
        'order_id': str(workflow.order_id),
        'stage': workflow.stage,
        'status': workflow.status,
        'started_at': workflow.started_at,
        'completed_at': workflow.completed_at,
        'notes': workflow.notes
    }), 200


@bp.route('/<uuid:workflow_id>', methods=['PUT'])
@token_required
def update_workflow(workflow_id):
    data = request.get_json()

    workflow = processing_workflow_service.update(
        workflow_id=workflow_id,
        data=data
    )

    if not workflow:
        return jsonify({
            'message': 'Processing workflow not found'
        }), 404

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


@bp.route('/<uuid:workflow_id>', methods=['DELETE'])
@token_required
def delete_workflow(workflow_id):
    deleted = processing_workflow_service.delete(workflow_id)

    if not deleted:
        return jsonify({
            'message': 'Processing workflow not found'
        }), 404

    return jsonify({
        'message': 'Processing workflow deleted successfully'
    }), 200