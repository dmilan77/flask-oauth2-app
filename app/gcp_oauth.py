from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import os
import secretloader
from google_auth_oauthlib.flow import Flow
from google.cloud import bigquery
from requests_oauthlib import OAuth2Session
from google.cloud import bigquery



app = Flask(__name__)


# This information is obtained upon registration of a new google OAuth
# application here: https://google.com/settings/applications/new
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
authorization_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
token_url = "https://www.googleapis.com/oauth2/v4/token"
# scopes = [
#      "https://www.googleapis.com/auth/userinfo.email",
#      "https://www.googleapis.com/auth/userinfo.profile",
#      "https://www.googleapis.com/auth/bigquery"
# ]
# scopes = ['email', 'profile']
scopes = 'openid https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/bigquery'    

redirect_uri = 'http://localhost:8080/callback'
project = "data-protection-01"



@app.route("/")
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. google)
    using an URL with a few key OAuth parameters.
    """
    # google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    google = Flow.from_client_secrets_file(
    'client_secrets.json',
    scopes=scopes,
    redirect_uri=redirect_uri)
    

    authorization_url, state = google.authorization_url(prompt='consent')

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
    state = session['oauth_state']
    google = Flow.from_client_secrets_file(
    'client_secrets.json',
    scopes=scopes,
    redirect_uri=redirect_uri,
    state=state)    
    print("**** Fetching Token .... ******")
    token = google.fetch_token(authorization_response=request.url)
    print("**** The Token ******")
    print(token)
    credentials = google.credentials
    print("**** The credentials ******")
    print(credentials)

    client = bigquery.Client(project=project, credentials=credentials)
    query_string = """SELECT firstname, lastname, zip
    FROM `data-protection-01.dataset1.verysecret`
    ;
    """
    query_job = client.query(query_string)

    # Print the results.
    # for row in query_job.result():  # Wait for the job to complete.
    #     print(row)
    #     # print("{}: {}: {}".format(row["firstname"], row["lastname"], row["zip"]))
    rows = query_job.result()  
    out=""
    for row in rows:
        out=out+'<br/>'+str(row)
    # json_obj = json.dumps(str(records))
    # print(out)
    return out

    # return redirect(url_for('.profile'))




if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

    app.secret_key = os.urandom(24)
    app.run(host="0.0.0.0",port="8080",debug=True)