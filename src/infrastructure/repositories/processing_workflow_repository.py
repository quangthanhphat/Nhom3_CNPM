from infrastructure.models.generated_models import ProcessingWorkflows
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class ProcessingWorkflowRepository:
    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def list_all(self):
        return self.session.query(ProcessingWorkflows).all()

    def get_by_id(self, workflow_id):
        return self.session.query(ProcessingWorkflows).filter(
            ProcessingWorkflows.id == workflow_id
        ).first()

    def create(self, workflow):
        self.session.add(workflow)
        self.session.commit()
        self.session.refresh(workflow)
        return workflow

    def update(self, workflow):
        self.session.commit()
        self.session.refresh(workflow)
        return workflow

    def delete(self, workflow):
        self.session.delete(workflow)
        self.session.commit()