async function get_login_link(talentID, clientID, code_challenge) {
    const authorize_url = `https://login.microsoftonline.com/${talentID}/oauth2/v2.0/authorize`;

    const query = {
        prompt: "login",
        client_id: clientID,
        response_type: "code",
        redirect_uri: "usthing://oauth-login", // Make sure this is correctly registered
        scope: "openid offline_access",
        code_challenge: code_challenge,
        code_challenge_method: "S256",
    };

    const queryString = new URLSearchParams(query).toString();
    
    return `${authorize_url}?${queryString}`;
}
