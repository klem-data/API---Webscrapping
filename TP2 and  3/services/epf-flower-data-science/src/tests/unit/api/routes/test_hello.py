import pytest
from fastapi.testclient import TestClient


class TestHelloRoute:
    @pytest.fixture
    def client(self) -> TestClient:
        """
        Test client for integration tests
        """

        from main import get_application

        app = get_application()

        client = TestClient(app, base_url="http://testserver")

        return client

    def test_hello(self, client):
        # Setup some test data
        name = "testuser"
        url = f"/hello/{name}"

        # Call the function to be tested
        response = client.get(url)

        # Assert the output
        assert response.status_code == 200
        assert response.json() == {
            "message": "Hello testuser, from fastapi test route !"
        }
