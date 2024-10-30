# Obtaining an HKUST Access Token

This document explains how to obtain an HKUST app API access token using a somewhat unconventional method, along with the underlying theory.

## Disclaimer

This method is for **EDUCATIONAL PURPOSES ONLY**.

Unauthorized access to HKUST resources violates university policy. Use this information responsibly and at your own risk.

> Please CAREFULLY read the HKUST rules and regulations before using this method.
> The author is not responsible for any consequences resulting from the use of this method.

Violating these rules may result in disciplinary action.

1. [Related Laws, Hong Kong](https://itsc.hkust.edu.hk/it-policies-guidelines/related-laws)
2. [Acceptable Use Policy](https://itsc.hkust.edu.hk/it-policies-guidelines/aup)
3. [Student Academic Integrity](https://registry.hkust.edu.hk/resource-library/regulations-student-academic-integrity)

This method can help you access authorized resources, but never use it for unauthorized access. Never access other people's accounts without their permission.

**Never share your access token.** It's like your password and must be kept secret. **Never use this method to access others' accounts without permission or use someone else's token for abusive actions, such as booking all library rooms.**

## How It Works

HKUST utilizes a CAS system and Microsoft Entra ID for authentication across its entire system.  Directly reversing Microsoft Entra ID web authentication isn't feasible because tokens generated through web browsers lack the `offline` scope. This means they cannot be programmatically revalidated and require manual user interaction through the Microsoft login website and DUO security for session extension.

However, a student project from the Business School called USThing has special access to HKUST's internal API.  Its Entra ID authentication *does* have `offline` scope. This allows for token revalidation directly, without client-side re-authorization, using a `refresh_token`.

Through reverse engineering, using the generated access token, we can utilize endpoints to manage school resources like library and facility bookings.  Moreover, the access token isn't limited to the USThing API. It's actually valid for *all* HKUST app APIs. This suggests that USThing uses the official HKUST Microsoft Entra ID.  Therefore, a USThing access token is functionally equivalent to a general HKUST system token, granting access to more HKUST APIs (w5.ab.ust.hk).

HKUST likely added a USThing Native Client redirect URL and enabled the `offline_access` scope for development purposes. This simplified USThing's development and prolonged usability, eliminating frequent logins. However, it also inadvertently created a gateway for unofficial access through reverse engineering.

Familiarity with OAuth, PKCE (Proof Key for Code Exchange), hashing, and Microsoft Entra ID (formerly Active Directory) is recommended for a comprehensive understanding of this process.

## FAQ: OAuth Security

Assuming you're familiar with PKCE and OAuth in general, this method resembles a Man-in-the-Middle (MITM) attack. However, PKCE is designed to be resistant to MITM attacks and network interception.  So, how can we still obtain necessary tokens like the authorization code and refresh token?  Because the account used is your own. PKCE protects against unauthorized application access, but it cannot prevent reverse engineering when you control the account.

The program acts like a legitimate application, similar to USThing.  Unlike client secrets, PKCE's `code_verifier` and `code_challenge` are not fixed. They are randomly generated and hashed within the application, preventing network interceptors from obtaining them.  However, if you own the account, you can generate these values yourself, mock the authorization request, and retrieve your own refresh and access tokens.

## Prerequisites

You will need two constants: `TenantID` and `ClientID`.

## PKCE Challenge Generation

1. **`code_verifier`:** Generate a random string between 64 and 128 characters long.  Store this securely for future token revalidation.
2. **`code_challenge`:** Calculate the SHA-256 hash of the `code_verifier` and then Base64 encode the result.

## Authorization Request

Construct an authorization URL in your browser:

```bash
https://login.microsoftonline.com/{TenantID}/oauth2/v2.0/authorize
```

Append the following query parameters:

```bash
code_challenge=<your_code_challenge>
code_challenge_method=S256
prompt=login
redirect_uri=<your_redirect_uri>
client_id=<your_client_id>
response_type=code
state=<random_string>
scope=openid%20offline_access
```

After successful login and authentication, your browser will redirect to the specified `redirect_uri`. Extract the `code` parameter from the redirected URL.

### Obtaining Tokens

Make a `POST` request to:

```bash
https://login.microsoftonline.com/{TenantID}/oauth2/v2.0/token
```

With the following data:

```bash
grant_type=authorization_code  // Use "refresh_token" for renewal
client_id=<your_client_id>
code_verifier=<your_code_verifier>
redirect_uri=<your_redirect_uri>
code=<authorization_code>       // Obtained from redirect; omit for refresh
// refresh_token=<refresh_token> // Use this when grant_type is refresh_token
```

Initially, this will return a refresh token (with a long expiry) and an access token. You can use the refresh token to periodically renew the access token until the refresh token itself expires.

## Usage of Demo Python Script

```bash
pip install -r requirements.txt
python main.py data.json
```

Your access token is stored in `data.json`, it expires in 1.5 hour.  You can use the refresh token to renew it.

### Renewing Access Token

```bash
python renew.py data.json
```

## References

- [PKCE RFC](https://tools.ietf.org/html/rfc7636)