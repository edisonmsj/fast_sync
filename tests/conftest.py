import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.models import table_registry


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def session():
    #    create_engine('sqlite:///:memory:'): cria um mecanismo de banco de
    #    dados SQLite em memória usando SQLAlchemy. Este mecanismo
    #    será usado para criar uma sessão de banco de dados para nossos
    #     testes.
    engine = create_engine('sqlite:///:memory:')
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
