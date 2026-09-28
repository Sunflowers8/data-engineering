import logging

import pandas as pd
import requests
from pydantic import BaseModel, ValidationError
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# -------------------------
# Logging Configuration
# -------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# -------------------------
# Pydantic Data Model
# -------------------------

class User(BaseModel):
    id: int
    name: str
    email: str


# -------------------------
# API Client
# -------------------------

class APIClient:

    def __init__(self):

        # Configure retry behavior
        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504]
        )

        adapter = HTTPAdapter(max_retries=retry)

        # Create HTTP session
        self.session = requests.Session()

        # Attach retry configuration
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def get(self, url: str):

        response = self.session.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        return response


# -------------------------
# API Extraction Function
# -------------------------

def extract_api_data(url: str) -> pd.DataFrame:

    try:
        logger.info("Requesting data from API")

        # Create API client object
        client = APIClient()

        # Request API data
        response = client.get(url)

        # Convert JSON response to Python data
        data = response.json()

        # Validate every record using Pydantic
        validated_users = [
            User(**record)
            for record in data
        ]

        logger.info(
            "Successfully validated %d records",
            len(validated_users)
        )

        # Convert nested JSON into DataFrame
        df = pd.json_normalize(data)

        logger.info(
            "Successfully extracted %d records",
            len(df)
        )

        return df

    except requests.RequestException as error:
        logger.error(
            "API request failed: %s",
            error
        )
        raise

    except ValidationError as error:
        logger.error(
            "Data validation failed: %s",
            error
        )
        raise


# -------------------------
# Run Script
# -------------------------

if __name__ == "__main__":

    url = "https://jsonplaceholder.typicode.com/users"

    df = extract_api_data(url)

    print(df.head())