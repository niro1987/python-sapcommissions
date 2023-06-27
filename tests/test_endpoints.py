import unittest
from unittest.mock import MagicMock, Mock, patch

from requests import HTTPError

from sapcommissions import Connection
from sapcommissions.endpoints import _Client, _Endpoint
from sapcommissions.exceptions import AuthenticationError, ClientError, ServerError


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = _Client("https://example.com", "username", "password")

    @patch("sapcommissions.endpoints.Session.request")
    def test_request_success(self, mocked_request):
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers.get.return_value = "application/json"
        mock_response.json.return_value = {"foo": "bar"}

        # Configure mock request to return mocked response
        mocked_request.return_value.__enter__.return_value = mock_response

        # Perform request
        result = self.client.request(
            method="GET",
            uri="/test",
            parameters={"param": "value"},
        )

        # Check that mock request was called with correct arguments
        mocked_request.assert_called_once_with(
            method="GET",
            url="https://example.com/test",
            params={"param": "value"},
            json=None,
        )

        # Check that client returned expected result
        self.assertEqual(result, {"foo": "bar"})

    @patch("sapcommissions.endpoints.Session.request")
    def test_request_error_not_json(self, mocked_request):
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers.get.return_value = "spam eggs"

        # Configure mock request to return mocked response
        mocked_request.return_value.__enter__.return_value = mock_response

        # Perform request
        with self.assertRaises(ValueError):
            self.client.request(
                method="GET",
                uri="/test",
                parameters={"param": "value"},
            )

        # Check that mock request was called with correct arguments
        mocked_request.assert_called_once_with(
            method="GET",
            url="https://example.com/test",
            params={"param": "value"},
            json=None,
        )

    @patch("sapcommissions.endpoints.Session.request")
    def test_request_error_400(self, mocked_request):
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.raise_for_status.side_effect = HTTPError

        # Configure mock request to return mocked response
        mocked_request.return_value.__enter__.return_value = mock_response

        # Perform request
        with self.assertRaises(ClientError):
            self.client.request(
                method="GET",
                uri="/test",
                parameters={"param": "value"},
            )

        # Check that mock request was called with correct arguments
        mocked_request.assert_called_once_with(
            method="GET",
            url="https://example.com/test",
            params={"param": "value"},
            json=None,
        )

    @patch("sapcommissions.endpoints.Session.request")
    def test_request_error_401(self, mocked_request):
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = HTTPError

        # Configure mock request to return mocked response
        mocked_request.return_value.__enter__.return_value = mock_response

        # Perform request
        with self.assertRaises(AuthenticationError):
            self.client.request(
                method="GET",
                uri="/test",
                parameters={"param": "value"},
            )

        # Check that mock request was called with correct arguments
        mocked_request.assert_called_once_with(
            method="GET",
            url="https://example.com/test",
            params={"param": "value"},
            json=None,
        )

    @patch("sapcommissions.endpoints.Session.request")
    def test_request_error_403(self, mocked_request):
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.raise_for_status.side_effect = HTTPError

        # Configure mock request to return mocked response
        mocked_request.return_value.__enter__.return_value = mock_response

        # Perform request
        with self.assertRaises(AuthenticationError):
            self.client.request(
                method="GET",
                uri="/test",
                parameters={"param": "value"},
            )

        # Check that mock request was called with correct arguments
        mocked_request.assert_called_once_with(
            method="GET",
            url="https://example.com/test",
            params={"param": "value"},
            json=None,
        )

    @patch("sapcommissions.endpoints.Session.request")
    def test_request_error_404(self, mocked_request):
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = HTTPError

        # Configure mock request to return mocked response
        mocked_request.return_value.__enter__.return_value = mock_response

        # Perform request
        with self.assertRaises(ClientError):
            self.client.request(
                method="GET",
                uri="/test",
                parameters={"param": "value"},
            )

        # Check that mock request was called with correct arguments
        mocked_request.assert_called_once_with(
            method="GET",
            url="https://example.com/test",
            params={"param": "value"},
            json=None,
        )

    @patch("sapcommissions.endpoints.Session.request")
    def test_request_error_412(self, mocked_request):
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = 412
        mock_response.raise_for_status.side_effect = HTTPError

        # Configure mock request to return mocked response
        mocked_request.return_value.__enter__.return_value = mock_response

        # Perform request
        with self.assertRaises(ClientError):
            self.client.request(
                method="GET",
                uri="/test",
                parameters={"param": "value"},
            )

        # Check that mock request was called with correct arguments
        mocked_request.assert_called_once_with(
            method="GET",
            url="https://example.com/test",
            params={"param": "value"},
            json=None,
        )

    @patch("sapcommissions.endpoints.Session.request")
    def test_request_error_500(self, mocked_request):
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = HTTPError

        # Configure mock request to return mocked response
        mocked_request.return_value.__enter__.return_value = mock_response

        # Perform request
        with self.assertRaises(ServerError):
            self.client.request(
                method="GET",
                uri="/test",
                parameters={"param": "value"},
            )

        # Check that mock request was called with correct arguments
        mocked_request.assert_called_once_with(
            method="GET",
            url="https://example.com/test",
            params={"param": "value"},
            json=None,
        )

    @patch("sapcommissions.endpoints.Session.request")
    def test_get_success(self, mocked_request):
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers.get.return_value = "application/json"
        mock_response.json.return_value = {"foo": "bar"}

        # Configure mock request to return mocked response
        mocked_request.return_value.__enter__.return_value = mock_response

        # Perform request
        result = self.client.get("/test")

        # Check that client returned expected result
        self.assertEqual(result, {"foo": "bar"})

    @patch("sapcommissions.endpoints.Session.request")
    def test_delete_success(self, mocked_request):
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers.get.return_value = "application/json"
        mock_response.json.return_value = {"foo": "bar"}

        # Configure mock request to return mocked response
        mocked_request.return_value.__enter__.return_value = mock_response

        # Perform request
        result = self.client.delete("/test")

        # Check that client returned expected result
        self.assertEqual(result, {"foo": "bar"})

    @patch("sapcommissions.endpoints.Session.request")
    def test_post_success(self, mocked_request):
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers.get.return_value = "application/json"
        mock_response.json.return_value = {"foo": "bar"}

        # Configure mock request to return mocked response
        mocked_request.return_value.__enter__.return_value = mock_response

        # Perform request
        result = self.client.post("/test", {"spam": "eggs"})

        # Check that client returned expected result
        self.assertEqual(result, {"foo": "bar"})

    @patch("sapcommissions.endpoints.Session.request")
    def test_put_success(self, mocked_request):
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers.get.return_value = "application/json"
        mock_response.json.return_value = {"foo": "bar"}

        # Configure mock request to return mocked response
        mocked_request.return_value.__enter__.return_value = mock_response

        # Perform request
        result = self.client.put("/test", {"spam": "eggs"})

        # Check that client returned expected result
        self.assertEqual(result, {"foo": "bar"})


class TestEndpoint(unittest.TestCase):
    def setUp(self):
        # Create a mock connection for testing
        self.connection = Connection("spam", "eggs", "user", "pass")

        # Create a mock resource to be used by the endpoint
        self.resource = Mock()
        self.resource._name = "test_resource"

        # Create the endpoint to test
        self.endpoint = _Endpoint(connection=self.connection)
        self.endpoint.resource = self.resource

    def test_name(self):
        # Check that the name property returns the correct value
        self.assertEqual(self.endpoint.name, "test_resource")

    def test_url(self):
        # Check that the url property returns the correct value
        self.assertEqual(self.endpoint.url, "/v2/test_resource")

    def test_init(self):
        # Check that the endpoint was initialized correctly
        self.assertEqual(
            self.endpoint._client.baseUrl,
            "https://spam-eggs.callidusondemand.com/api",
        )
        self.assertEqual(self.endpoint._client.auth.username, "user")
        self.assertEqual(self.endpoint._client.auth.password, "pass")
        self.assertTrue(self.endpoint._client.verify)


if __name__ == "__main__":
    unittest.main()
