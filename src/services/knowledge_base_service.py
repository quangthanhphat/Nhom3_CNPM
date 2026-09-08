from infrastructure.models.generated_models import KnowledgeBase


class KnowledgeBaseService:

    def __init__(self, repository):
        self.repository = repository

    def list_for_user(self, user_id, is_admin=False):
        if is_admin:
            return self.repository.list_all()

        return self.repository.get_by_author_id(user_id)

    def get_by_id_for_user(
        self,
        knowledge_id,
        user_id,
        is_admin=False
    ):
        knowledge = self.repository.get_by_id(knowledge_id)

        if not knowledge:
            return None, "Knowledge base entry not found"

        if not is_admin and knowledge.author_id != user_id:
            return None, "Access denied"

        return knowledge, None

    def create(self, user_id, data):
        knowledge = KnowledgeBase(
            author_id=user_id,
            title=data.get("title"),
            content=data.get("content"),
            status=data.get("status", "draft"),
            post_id=data.get("post_id")
        )

        return self.repository.create(knowledge), None

    def update(
        self,
        knowledge_id,
        user_id,
        data,
        is_admin=False
    ):
        knowledge, error = self.get_by_id_for_user(
            knowledge_id,
            user_id,
            is_admin
        )

        if error:
            return None, error

        if "title" in data:
            knowledge.title = data["title"]

        if "content" in data:
            knowledge.content = data["content"]

        if "post_id" in data:
            knowledge.post_id = data["post_id"]

        if is_admin and "status" in data:
            knowledge.status = data["status"]

        return self.repository.update(knowledge), None

    def delete(
        self,
        knowledge_id,
        user_id,
        is_admin=False
    ):
        knowledge, error = self.get_by_id_for_user(
            knowledge_id,
            user_id,
            is_admin
        )

        if error:
            return False, error

        self.repository.delete(knowledge)

        return True, None