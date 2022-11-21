from typing import List

import httpx

from .config import API_LIST_URL


def get_api_list() -> List[str]:
    response = httpx.get(API_LIST_URL)
    return response.json()
