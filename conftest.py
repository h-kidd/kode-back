import pytest
import server

@pytest.fixture
def api():
    api = server.app.test_client()
    return api