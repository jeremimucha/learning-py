from models import (
    complaint,
    State,
    RoleType
)
from db import database


class ComplaintManager:
    @staticmethod
    async def get_complaints(user: dict):
        q = complaint.select()
        user_role = user['role']
        user_id = user['id']
        if user_role == RoleType.complainer:
            q = q.where(complaint.c.complainer_id == user_id)
        elif user_role == RoleType.approver:
            q = q.where(complaint.c.status == State.pending)
        # elif user_role == RoleType.admin:
        # Oherwise we're an admin - do not resctict the query - get all complaints
        return await database.fetch_all(q)

    @staticmethod
    async def create_complaint(complaint_data: dict, user: dict):
        complaint_data['complainer_id'] = user['id']
        id_ = await database.execute(complaint.insert().values(complaint_data))
        return await database.fetch_one(complaint.select().where(complaint.c.id == id_))

    @staticmethod
    async def delete(complaint_id):
        await database.execute(complaint.delete().where(complaint.c.id == complaint_id))

    @staticmethod
    async def approve(complaint_id):
        await database.execute(complaint.update().where(complaint.c.id == complaint_id).values(status=State.approved))

    @staticmethod
    async def reject(complaint_id):
        await database.execute(complaint.update().where(complaint.c.id == complaint_id).values(status=State.rejected))
