from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    new_user = User(username='alice', password='secret', email='teste@test')
    session.add(new_user)
    session.commit()
    # O método .scalar é usado para performar buscas no banco (queries).
    # Ele pega o primeiro resultado da busca e faz uma
    #  operação de converter o resultado do banco de dados em um Objeto criado
    #  pelo SQLAlchemy, nesse caso, caso encontre
    #  um resultado, ele irá converter na classe User. A função de select é uma
    #  função de busca de dados no banco. Nesse
    #  caso estamos procurando em todos os Users onde (where) o nome é igual a
    #  "alice".
    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'
