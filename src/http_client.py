import logging
from typing import Dict, Optional

import requests
from requests import HTTPError


class HttpClient:
    def __init__(self, headers: Dict):
        self._headers = headers

    def post(self, url: str, payload: Dict, response_json_path: Optional[list[str]] = None) -> Dict:
        response = requests.post(url, headers=self._headers, json=payload)
        code = response.status_code

        if 200 <= code < 300:
            json_response = response.json()
            if response_json_path is not None:
                for path in response_json_path:
                    json_response = json_response[path]
            return json_response
        else:
            logging.error(f"post {url}: code received: {code} (reason: {response.reason})")
            raise HTTPError(response.reason)
