from fastapi import APIRouter,Depends
from app.services.assignment_service import accept_assignment_driver,get_assignmnet_driver
from app.schemas.assignment_schemas import AssignmentResponse
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.auth.dep import get_current_user
from app.models.user import User

assignment_router = APIRouter(
    tags=["Assignment"]
)

@assignment_router.get ("/my/assignments", response_model=AssignmentResponse)
def get_my_assignments (db:Session = Depends(get_db),user:User = Depends(get_current_user)):
    return get_assignmnet_driver(db,user)

@assignment_router.post("/assignmnts/{assignment_id}/accept",response_model=AssignmentResponse)
def accept_assignment (assignment_id:int,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    return accept_assignment_driver(db,user,assignment_id)