from fastapi import APIRouter

router = APIRouter(prefix='/todos', tags=['todos'])


@router.post('/', response_model=TodoPublic)
def create_todo(todo: TodoSchema):
    return {'message': 'Todo created'}