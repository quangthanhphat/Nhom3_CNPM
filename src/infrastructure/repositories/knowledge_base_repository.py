from infrastructure.models.generated_models import KnowledgeBase
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class KnowledgeBaseRepository:

    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def list_all(self):
        return self.session.query(KnowledgeBase).all()

    def get_by_id(self, knowledge_id):
        return self.session.query(KnowledgeBase).filter(
            KnowledgeBase.id == knowledge_id
        ).first()

    def get_by_author_id(self, author_id):
        return self.session.query(KnowledgeBase).filter(
            KnowledgeBase.author_id == author_id
        ).all()

    def create(self, knowledge):
        self.session.add(knowledge)
        self.session.commit()
        self.session.refresh(knowledge)

        return knowledge

    def update(self, knowledge):
        self.session.commit()
        self.session.refresh(knowledge)

        return knowledge

    def delete(self, knowledge):
        self.session.delete(knowledge)
        self.session.commit()