import pytest
from app import app  

@pytest.fixture
def client():
    """
    Create a test client for our app.

    :return: a test client
    """
    with app.test_client() as client:
        yield client

def test_gen_custom_sub(client):
    """
    Tests our key routes in the app.

    :return: None
    """
    # Test with a valid subreddit
    response = client.get('/rss/funny')
    assert response.status_code == 200
    assert b'funny' in response.data

    # Test with another subreddit with no self
    response = client.get('/rss/noself/python')
    assert response.status_code == 200
    assert b'python' in response.data

    # Test with an invalid URL
    response = client.get('/rss/asdfasgawertf')
    assert response.status_code == 404
    assert b'does not exist' in response.data

    # Test with an invalid URL, noself endpoint
    response = client.get('/rss/noself/asdfasgawertf')
    assert response.status_code == 404
    assert b'does not exist' in response.data

    # Test our healthcheck endpoint
    response = client.get('/healthcheck')
    assert response.status_code == 200
    assert b'reddit' in response.data
