import os
import disnake
import json
import requests

from datetime import datetime
from typing import Mapping


# GET environement variables
APIPASSWORD = os.environ["APIPASSWORD"]
APIUSERNAME = os.environ["APIUSERNAME"]


class StfuApi:
    def __init__(self):
        self._auth = (APIUSERNAME, APIPASSWORD)
        self._url = "https://api.stfurequiem.com/"

    def get_user_detail(self, user_id: int) -> dict:
        params = {"user_id": f"{user_id}"}
        response = requests.get(
            f"{self._url}discordusers", auth=self._auth, params=params
        )
        return response.json()
