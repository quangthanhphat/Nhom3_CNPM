from infrastructure.models.generated_models import ProcessingWorkflows
from infrastructure.repositories.processing_workflow_repository import (
    ProcessingWorkflowRepository
)
from infrastructure.repositories.order_repository import OrderRepository
from infrastructure.repositories.film_lab_repository import FilmLabRepository


class ProcessingWorkflowService:
    def __init__(self):
        self.repository = ProcessingWorkflowRepository()
        self.order_repository = OrderRepository()
        self.film_lab_repository = FilmLabRepository()

    def list_all(self):
        return self.repository.list_all()

    def list_for_user(self, user_id, role):
        workflows = self.repository.list_all()

        # Admin được xem tất cả
        if role == 'admin':
            return workflows

        result = []

        for workflow in workflows:
            order = self.order_repository.get_by_id(
                workflow.order_id
            )

            if not order:
                continue

            # Customer chỉ xem workflow của order mình
            if role == 'customer':
                if str(order.customer_id) == str(user_id):
                    result.append(workflow)

            # Film Lab Owner chỉ xem workflow
            # của các order thuộc Film Lab của mình
            elif role == 'film_lab_owner':
                film_lab = self.film_lab_repository.get_by_id(
                    order.film_lab_id
                )

                if (
                    film_lab
                    and str(film_lab.owner_id) == str(user_id)
                ):
                    result.append(workflow)

        return result

    def get_by_id(self, workflow_id):
        return self.repository.get_by_id(workflow_id)

    def get_by_id_for_user(self, workflow_id, user_id, role):
        workflow = self.repository.get_by_id(workflow_id)

        if not workflow:
            return None, 'not_found'

        # Admin được xem tất cả
        if role == 'admin':
            return workflow, None

        order = self.order_repository.get_by_id(
            workflow.order_id
        )

        if not order:
            return None, 'not_found'

        # Customer chỉ xem workflow của order mình
        if role == 'customer':
            if str(order.customer_id) != str(user_id):
                return None, 'forbidden'

            return workflow, None

        # Film Lab Owner chỉ xem workflow
        # của order thuộc lab của mình
        if role == 'film_lab_owner':
            film_lab = self.film_lab_repository.get_by_id(
                order.film_lab_id
            )

            if not film_lab:
                return None, 'forbidden'

            if str(film_lab.owner_id) != str(user_id):
                return None, 'forbidden'

            return workflow, None

        return None, 'forbidden'

    def create(self, data, user_id, role):
        order_id = data.get('order_id')

        order = self.order_repository.get_by_id(order_id)

        if not order:
            return None, 'order_not_found'

        # Admin được tạo workflow cho mọi order
        if role == 'admin':
            pass

        # Film Lab Owner chỉ được tạo workflow
        # cho order thuộc Film Lab của mình
        elif role == 'film_lab_owner':
            film_lab = self.film_lab_repository.get_by_id(
                order.film_lab_id
            )

            if not film_lab:
                return None, 'forbidden'

            if str(film_lab.owner_id) != str(user_id):
                return None, 'forbidden'

        else:
            return None, 'forbidden'

        workflow = ProcessingWorkflows(
            order_id=order_id,
            stage=data.get('stage'),
            status=data.get('status'),
            started_at=data.get('started_at'),
            completed_at=data.get('completed_at'),
            notes=data.get('notes')
        )

        return self.repository.create(workflow), None

    def update(
        self,
        workflow_id,
        data,
        user_id,
        role
    ):
        workflow, error = self.get_by_id_for_user(
            workflow_id=workflow_id,
            user_id=user_id,
            role=role
        )

        if error:
            return None, error

        # Nếu có thay đổi order_id thì phải kiểm tra
        # order mới cũng thuộc quyền quản lý.
        new_order_id = data.get('order_id')

        if new_order_id:
            new_order = self.order_repository.get_by_id(
                new_order_id
            )

            if not new_order:
                return None, 'order_not_found'

            if role != 'admin':
                film_lab = self.film_lab_repository.get_by_id(
                    new_order.film_lab_id
                )

                if (
                    not film_lab
                    or str(film_lab.owner_id) != str(user_id)
                ):
                    return None, 'forbidden'

            workflow.order_id = new_order_id

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

        return self.repository.update(workflow), None

    def delete(
        self,
        workflow_id,
        user_id,
        role
    ):
        workflow, error = self.get_by_id_for_user(
            workflow_id=workflow_id,
            user_id=user_id,
            role=role
        )

        if error:
            return False, error

        self.repository.delete(workflow)

        return True, None