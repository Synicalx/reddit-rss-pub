import pytest
from app import app  

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_gen_custom_sub(client):
    # Test with a valid subreddit
    response = client.get('/rss/funny')
    assert response.status_code == 200
    assert b'funny' in response.data

    # Test with another subreddit
    response = client.get('/rss/python')
    assert response.status_code == 200
    assert b'python' in response.data

    # Test with an invalid URL
    response = client.get('/rss/asdfasgawertf')
    assert response.status_code == 404
    assert b'does not exist' in response.data