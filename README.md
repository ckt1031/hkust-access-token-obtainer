# hkust-access-token-obtainer

Obtaining HKUST app API with tricky way and theory explained

You need two constants: `TenantID` and `ClientID`.

## PKCE Challenge

A random string as `code_verifier` between 64 and 128 characters in length; it is best to store this for future revalidation.  
`code_challenge`: Base64 encoded SHA-256 hash of `code_verifier`.

## Authorization

Create an authorization string:

```
BROWSER https://login.microsoftonline.com/{TenantID}/oauth2/v2.0/authorize
```

With specific queries:

```bash
code_challenge=
code_challenge_method=S256
prompt=login
redirect_uri=
client_id=
response_type=code
state= # Random String
scope=openid%20offline_access
```

In the browser, if you are logged in and validated, you will be redirected to a specified URL, and you need to retrieve the `code` query value from your redirection URL.

## Obtaining Refresh and Access Tokens

```
POST https://login.microsoftonline.com/{TenantID}/oauth2/v2.0/token
```

```bash
grant_type=authorization_code # switch to refresh_token for renewing access tokens using a refresh token
client_id=
code_verifier= # Where your stored random string is
redirect_uri= 
code= # Just obtained from the redirection URL; comment this out if grant_type=refresh_token
# refresh_token= # Uncomment this if grant_type is refresh_token
```

First, you will get the refresh token (which should have a very long expiry), and you can revalidate your access token until the "very long validation" ends.
