from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_root_must_return_ok_e_html():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK

    content_type = response.headers.get('Content-Type')
    assert 'text/html' in content_type, 'Content-Type is not HTML'

    assert (
        '<html' in response.text.lower()
    ), 'Response does not contain <html> tag'
    assert (
        '</html>' in response.text.lower()
    ), 'Response does not contain </html> tag'


def test_create_user():
    client = TestClient(app)

    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }
