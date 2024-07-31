import json
from http import HTTPStatus
import requests

class Token:
    def __init__(
        self, app_acess, refresh_token, client_id, client_secret
    ) -> None:
        self.__app_access = app_acess
        self.__refresh_token = refresh_token
        self.__client_id = client_id
        self.__client_secret = client_secret
        
    def make_request(self, url):
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.get_app_access()}"
            }

        response = requests.get(url, headers=headers)
        try:
            return json.loads(response.text)
        except:
            print(response.text)

    def get_new_token_with_refresh(self):
        data = {
            "client_id": self.__client_id,
            "client_secret": self.__client_secret,
            "refresh_token": self.__refresh_token,
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }
        response = requests.post(
            "https://api.rd.services/auth/token",
            headers=headers,
            json=data,
        )
        data_response = json.loads(response.text)
        if response.status_code == HTTPStatus.BAD_REQUEST:
            return data_response

        newAppAccess = data_response["access_token"]
        newRefreshToken = data_response["refresh_token"]

        
        self.set_app_access(newAppAccess)
        self.set_refresh_token(newRefreshToken)
        self.update_env(newRefreshToken, newAppAccess)

        return "OK"
    
    def get_new_token_with_code(self, code):
        url = "https://api.rd.services/auth/token?token_by=code"

        payload = {
            "client_id": self.__client_id,
            "client_secret": self.__client_secret,
            "code": code
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        data_response = json.loads(response.text)
        
        newAppAccess = data_response["access_token"]
        newRefreshToken = data_response["refresh_token"]
    
        self.set_app_access(newAppAccess)
        self.set_refresh_token(newRefreshToken)
        self.update_env(newRefreshToken, newAppAccess)

    def get_app_access(self) -> str:
        return self.__app_access

    def get_refresh_token(self) -> str:
        return self.__refresh_token

    def set_app_access(self, app_access: str) -> None:
        self.__app_access = app_access

    def set_refresh_token(self, refresh_token: str) -> None:
        self.__refresh_token = refresh_token

    def update_env(self, refresh_token: str, app_access: str):
        env = open("./.env", "w")
        lines = [
            f"client_secret='{self.__client_secret}' \n",
            f"client_id='{self.__client_id}'\n",
            f"refresh_token='{refresh_token}'\n",
            f"app_access='{app_access}'\n",
        ]
        env.writelines(lines)
        env.close()