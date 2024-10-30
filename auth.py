import webbrowser
from urllib.parse import urlencode

import pkce
import requests

from api import get_user_info
from constant import clientID, talentID
from file import save_file

code_verifier = pkce.generate_code_verifier(length=128)
code_challenge = pkce.get_code_challenge(code_verifier)


def get_login_link():
    authorize_url = (
        f"https://login.microsoftonline.com/{talentID}/oauth2/v2.0/authorize"
    )

    query = {
        "prompt": "login",
        "client_id": clientID,
        "response_type": "code",
        "redirect_uri": "usthing://oauth-login",
        "scope": "openid offline_access",
        # PKCE
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    return f"{authorize_url}?{urlencode(query)}"


def microsoft_token(code: str, code_verifier: str, refresh_token: str) -> str:
    token_url = f"https://login.microsoftonline.com/{talentID}/oauth2/v2.0/token"

    formBody = {
        "client_id": clientID,
        "code": code,
        "grant_type": "authorization_code" if refresh_token == "" else "refresh_token",
        "redirect_uri": "usthing://oauth-login",
        "code_verifier": code_verifier,
    }

    if refresh_token != "":
        formBody["refresh_token"] = refresh_token

    response = requests.post(
        token_url,
        data=formBody,
        timeout=10,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    return response.json()


def parse_usthing_redirection(redirect_url: str) -> str:
    query = redirect_url.split("?")[1]
    query = dict(q.split("=") for q in query.split("&"))

    return query["code"]


if __name__ == "__main__":
    login_url = get_login_link()
    print(
        "Opening in browser, if no browser tab opened, paste this URL into the browser: "
        + login_url
    )
    webbrowser.open(login_url)

    redirect_code = input("Paste the redirect URL here (usthing://.../): ")

    code = parse_usthing_redirection(redirect_code)

    response = microsoft_token(code, code_verifier, "")

    local_data_to_save = {
        "code_verifier": code_verifier,
        "code": code,
        "access_token": response["access_token"],
        "refresh_token": response["refresh_token"],
    }

    # Test first
    data = get_user_info(response["access_token"])

    print(f"Hello, {data['displayName']}")

    save_file(local_data_to_save)

    print("Token saved! Expires in 1.5 hour.")
