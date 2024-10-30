import requests


def get_user_info(token: str):
    url = "https://graph.microsoft.com/v1.0/me"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)

    return response.json()
