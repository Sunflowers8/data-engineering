import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.append(
    str(Path(__file__).parent.parent / "src")
)

from pipeline.api_extract import APIClient, extract_api_data


def test_api_client_creation():
    client = APIClient()

    assert client.session is not None


def test_mock_response():
    mock_response = Mock()

    mock_response.status_code = 200

    assert mock_response.status_code == 200


def test_extract_api_data():
    fake_data = [
        {
            "id": 1,
            "name": "Simran",
            "email": "simran@example.com"
        }
    ]

    mock_response = Mock()
    mock_response.json.return_value = fake_data

    with patch(
        "pipeline.api_extract.APIClient.get",
        return_value=mock_response
    ):
        df = extract_api_data("https://fake-api.com/users")

    assert len(df) == 1
    assert df.iloc[0]["name"] == "Simran"
    assert df.iloc[0]["email"] == "simran@example.com"