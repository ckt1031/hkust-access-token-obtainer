from api import get_user_info
from auth import microsoft_token
from file import load_file, save_file

if __name__ == "__main__":
    data = load_file()

    code = data["code"]
    code_verifier = data["code_verifier"]
    refresh_token = data["refresh_token"]

    response = microsoft_token(code, code_verifier, refresh_token)

    # Test first
    data = get_user_info(response["access_token"])

    print(f"Welcome back, {data['displayName']}!")

    data_to_save = {
        "code_verifier": code_verifier,
        "code": code,
        "access_token": response["access_token"],
        "refresh_token": response["refresh_token"],
    }

    save_file(data_to_save)
