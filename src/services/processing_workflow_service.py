from infrastructure.models.generated_models import ProcessingWorkflows
from infrastructure.repositories.processing_workflow_repository import (
    ProcessingWorkflowRepository
)


class ProcessingWorkflowService:
    def __init__(self):
        self.repository = ProcessingWorkflowRepository()

    def list_all(self):
        return self.repository.list_all()

    def get_by_id(self, workflow_id):
        return self.repository.get_by_id(workflow_id)

    def create(self, data):
        workflow = ProcessingWorkflows(
            order_id=data.get('order_id'),
            stage=data.get('stage'),
            status=data.get('status'),
            started_at=data.get('started_at'),
            completed_at=data.get('completed_at'),
            notes=data.get('notes')
        )

        return self.repository.create(workflow)

    def update(self, workflow_id, data):
        workflow = self.repository.get_by_id(workflow_id)

        if not workflow:
            return None

        workflow.order_id = data.get(
            'order_id',
            workflow.order_id
        )
        workflow.stage = data.get(
            'stage',
            workflow.stage
        )
        workflow.status = data.get(
            'status',
            workflow.status
        )
        workflow.started_at = data.get(
            'started_at',
            workflow.started_at
        )
        workflow.completed_at = data.get(
            'completed_at',
            workflow.completed_at
        )
        workflow.notes = data.get(
            'notes',
            workflow.notes
        )

        return self.repository.update(workflow)

    def delete(self, workflow_id):
        workflow = self.repository.get_by_id(workflow_id)

        if not workflow:
            return False

        self.repository.delete(workflow)

        return True