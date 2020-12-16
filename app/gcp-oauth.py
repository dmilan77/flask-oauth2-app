from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import os
import secretloader

app = Flask(__name__)


# This information is obtained upon registration of a new google OAuth
# application here: https://google.com/settings/applications/new
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
authorization_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
token_url = "https://www.googleapis.com/oauth2/v4/token"
scope = [
     "https://www.googleapis.com/auth/userinfo.email",
     "https://www.googleapis.com/auth/userinfo.profile",
     "https://www.googleapis.com/auth/bigquery"
]
redirect_uri = 'http://localhost:8080/callback'



@app.route("/")
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. google)
    using an URL with a few key OAuth parameters.
    """
    google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    authorization_url, state = google.authorization_url(authorization_base_url,
            access_type="offline", prompt="select_account")

    session['oauth_state'] = state
    # return redirect(authorization_url)
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.

@app.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """
    # print('Getting back from callvack :')
    google = OAuth2Session(client_id, state=session['oauth_state'],redirect_uri=redirect_uri)
    token = google.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)
    print("**** The Token ******")
    print(token)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    session['oauth_token'] = token

    return redirect(url_for('.profile'))


@app.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 2 token.
    """
    google = OAuth2Session(client_id, token=session['oauth_token'])

    return  jsonify(google.get('https://www.googleapis.com/oauth2/v3/userinfo').json())


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

    app.secret_key = os.urandom(24)
    app.run(host="0.0.0.0",port="8080",debug=True)