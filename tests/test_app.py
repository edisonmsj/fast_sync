from http import HTTPStatus


def test_root_must_return_ok_e_html(client):
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


def test_post_username_duplicated(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@test.com',
            'password': 'secrett',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_post_email_duplicated(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'teste@test.com',
            'password': 'secrett',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
