from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import TodoPublic, TodoSchema
from fast_zero.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])

T_Session = Annotated[Session, Depends(get_session)]
T_User = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=TodoPublic)
def create_todo(todo: TodoSchema, user: T_User, session: T_Session):
    return todo
