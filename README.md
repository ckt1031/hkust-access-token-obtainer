# HKUST Access Token Obtainer

Obtaining HKUST app API with tricky way and theory explained.

## Theory

In general, HKUST uses CAS system and Microsoft Entra ID for authentication across their whole system. In fact that, we are not abled to reverse Microsoft Entra ID web authentication directly, because those tokens generated through web browsers do not have `offline` scope access, in other words, they cannot be revalidated itself programmatically, ot requires real human to extend their session again through real Microsoft authentication progress, like where you see the Microsoft login website and DUO security.

However, there is an app developed by Business School, a student project called USThing, which has special access to HKUST internal API where it's Entra ID authentication has `offline` scope, this means they (Me) are abled to revalidate tokens directly without re-authorization on the client by using special token called `refresh_token`.

Based on general network reverse engineering techniques, by using the access token generated, we can utilise some cool endpoints which are abled to directly manage school stuffs like library and facilities booking.

Aside from that, surprisingly, access token generated below isn't only for USThing API itself, it was actually accessible for all HKUST app APIs, I realized that the Microsoft Entra ID of USThing was actually the one of HKUST official one, that's mean USThing access token is equivalent to HKUST system token, that's mean we can use USThing API token to access more HKUST APIs (w5.ab.ust.hk).

HKUST more likely extraly added USThing Native Client redirect URL and allow offline access scope for their development. This made USThing more easier to develop and use for longevity instead of logging in every few hours, while this opened a gateway for easy reverse engineering and access in non official way.

In order to understand the entire project, you must be familiar with OAuth, PKCE Challenge, Hashing and Microsoft Entra ID (formerly Active Directory).

## FAQ on OAuth Security

Assume you are aware of PKCE and general OAuth.

Actually you are undergoing Man-in-the-Middle Attack to intercept the OAuth, but the truth is that PKCE is resilient to MITM Attack or any network interception. Why we can still get all required tokens like code, and refresh token? The answer is the account is yours, PKCE are not abled to project applications from being reversed if the application account is owned by you or accessibile by you, this is the point, simple.

The program in the repository is to act as a real application like USThing. PKCE's code verifier and code challenge are not fixed secret on any platforms, unlike client secret. It has just a random string generated and hashed string on applications that was unabled for network incepters to obtain, but if the login account is yours and you CAN generate yourself to make mocked authorization request and get your own refresh and access token.

## Perquisites

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
