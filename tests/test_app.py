from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_root_deve_retornar_ok_e_html():
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
