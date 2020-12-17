from google_auth_oauthlib.flow import Flow

# Create the flow using the client secrets file from the Google API
# Console.
scopes = 'openid https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/bigquery'    

flow = Flow.from_client_secrets_file(
    'client_secret_desktop_client.com.json',
    scopes=scopes,
    redirect_uri='urn:ietf:wg:oauth:2.0:oob')

# Tell the user to go to the authorization URL.
auth_url, _ = flow.authorization_url(prompt='consent')

print('Please go to this URL: {}'.format(auth_url))

# The user will get an authorization code. This code is used to get the
# access token.
code = input('Enter the authorization code: ')
flow.fetch_token(code=code)

# You can use flow.credentials, or you can just get a requests session
# using flow.authorized_session.
session = flow.authorized_session()
print(session.get('https://www.googleapis.com/userinfo/v2/me').json())

from google.cloud import bigquery

project = "data-protection-01"
query_string = """SELECT firstname, lastname, zip
    FROM `data-protection-01.dataset1.verysecret`
    ;
"""

client = bigquery.Client(project=project, credentials=flow.credentials)
query_job = client.query(query_string)

rows = query_job.result()  

for row in rows:
   print(row)
