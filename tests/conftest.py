import factory
import factory.fuzzy
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import Todo, TodoState, User, table_registry
from fast_zero.security import get_password_hash


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user_{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}+senha')


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker('text')
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    #    create_engine('sqlite:///:memory:'): cria um mecanismo de banco de
    #    dados SQLite em memória usando SQLAlchemy. Este mecanismo
    #    será usado para criar uma sessão de banco de dados para nossos
    #     testes.
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    #    table_registry.metadata.create_all(engine): cria todas as tabelas no
    #    banco de dados de teste antes de cada teste
    #     usa a fixture session.
    table_registry.metadata.create_all(engine)

    #    Session(engine): cria uma sessão Session para que os testes possam se
    #     comunicar com o banco de dados. Por conta do
    #     yield a sessão é sempre renovada após cada teste.
    with Session(engine) as session:
        #    yield Session(): fornece uma instância de Session que será
        #    injetada em cada teste que solicita a fixture session. Essa
        #    sessão será usada para interagir com o banco de dados de teste.
        yield session
    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    pwd = 'secret'
    user = UserFactory(
        password=get_password_hash(pwd),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd  # Monkey Patch

    return user


@pytest.fixture()
def other_user(session):
    user = UserFactory()

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture()
def token(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': user.username,
            'password': user.clean_password,
        },
    )

    return response.json()['access_token']
