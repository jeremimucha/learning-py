from typing import List
from fastapi import (
    APIRouter,
    Depends,
)
from starlette.requests import Request

from managers.complaint import ComplaintManager
from managers.auth import (oauth2_scheme, is_complainer, is_admin, is_approver)
from schemas.request.complaint import ComplaintIn
from schemas.response.complaint import ComplaintOut


router = APIRouter(tags=["Complaints"])


@router.get("/complaints/", dependencies=[Depends(oauth2_scheme)], response_model=List[ComplaintOut])
async def get_complaints(request: Request):
    user = request.state.user
    return await ComplaintManager.get_complaints(user)


@router.post("/complaints/", dependencies=[Depends(oauth2_scheme), Depends(is_complainer)], response_model=ComplaintOut)
async def create_complaint(request: Request, complaint: ComplaintIn):
    user = request.state.user
    return await ComplaintManager.create_complaint(complaint.dict(), user)


@router.delete(
    "/complaints/{complaint_id}/",  # parameterized request, accepting the complaint_id to delete
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],  # user needs to be both authenticated and authorized
    status_code=204,  # requests returning no content should return the status code `204: No Content`
)
# fastapi will transform the complaint_id string from request into an into parameter (based on the given type hint)
async def delete_complaint(complaint_id: int):
    await ComplaintManager.delete(complaint_id)


@router.put(
    "/complaints/{complaint_id}/approve",
    dependencies=[Depends(oauth2_scheme), Depends(is_approver)],
    status_code=204,
)
async def approve_complaint(complaint_id: int):
    await ComplaintManager.approve(complaint_id)


@router.put(
    "/complaints/{complaint_id}/reject",
    dependencies=[Depends(oauth2_scheme), Depends(is_approver)],
    status_code=204,
)
async def reject_complaint(complaint_id: int):
    await ComplaintManager.reject(complaint_id)
