from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fast_zero.models import User

from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from fast_zero.settings import Settings

app = FastAPI()


@app.get('/', response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hello World</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background: linear-gradient(to right, #ff7e5f, #feb47b);
                font-family: 'Arial', sans-serif;
            }
            .container {
                text-align: center;
                color: #fff;
            }
            h1 {
                font-size: 4em;
                animation: fadeIn 3s ease-in-out;
            }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Olá Mundo</h1>
        </div>
    </body>
    </html>
    """


database = []


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    engine = create_engine(Settings().DATABASE_URL)

    with Session(engine) as session:
        db_user = session.scalar(
            select(User).where(
               (User.username == user.username) | (User.email == user.email))
        )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    db_user = User(
        username=user.username, password=user.password, email=user.email
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {'users': database}


@app.get('/users/{id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def read_user(id: int):
    return database[id - 1]


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    del database[user_id - 1]

    return {'message': 'User deleted'}
