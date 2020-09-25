from flask import Blueprint, request, redirect, url_for, session
from flask import current_app as app
import requests
import mf2py

# blueprint configuration
auth_bp = Blueprint('auth_bp', __name__)
state = app.config['SESSION_SECRET']

# Steps:
#
# 1. GET  /login    opens a login view that posts to the same route.
# 2. POST /login    builds uri redirect to github auth endpoint. After authorization, Github redirects to /callback with an auth code.
# 3. GET  /callback sends auth code to token endpoint, stores token in session, then redirects to final route.
# 4. GET  /create   does whatever I want

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return """
        <form method=post action=/login>
            <input type=url id=me name=me />
            <input type=submit value=Submit />
            </form>"""
    else:
        # error checks
        if 'me' not in request.form:
            redirect(url_for('auth_bp.login'))
        if request.form['me'] != 'https://alexbilson.dev':
            return f"{request.form['me']} is not on the list of authorized sites."

        session['me'] = request.form['me']
        params = get_site_params(request.form['me'])

        if not params['success']:
            return "<br />".join(params['messages'])

        uri = create_auth_uri()
        return redirect(uri)

@auth_bp.route('/callback', methods=['GET'])
def callback():
    # error checks
    if 'state' not in request.args:
        return "no state was present. aborting auth."
    if 'code' not in request.args:
        return "no code was present. aborting auth."
    if request.args['state'] != state:
        return "the state does not match the auth request. aborting auth."

    session['access_token'] = get_token(request.args['code'])
    user_uri = get_user_uri(session['access_token'])

    # verifies github's id matches me
    if session['me'] != user_uri:
        return "your authorization endpoint does not match your entry. aborting."

    return redirect(url_for('micropub_bp.create'))

def get_site_params(site):
    resp = { 'success': False, 'messages': [], 'endpoints': {}}
    site = mf2py.parse(url=request.form['me'])

    if 'rels' not in site:
        resp['messages'].append("your site contains no relational links (rels).")
        return resp

    if 'token_endpoint' not in site['rels']:
        resp['messages'].append("your site contains no token endpoint. please add a header link with rel='token_endpoint'.")

    if 'authorization_endpoint' not in site['rels']:
        resp['messages'].append("your site contains no authorization endpoint. please add a header link with rel='authorization_endpoint'.")

    if 'micropub' not in site['rels']:
        resp['messages'].append("your site contains no authorization endpoint. please add a header link with rel='authorization_endpoint'.")

    if len(resp['messages']) > 0:
        return resp

    resp['endpoints']['token_endpoint'] = site['rels']['token_endpoint'][0]
    resp['endpoints']['auth_endpoint'] = site['rels']['authorization_endpoint'][0]
    resp['endpoints']['micropub_endpoint'] = site['rels']['micropub'][0]
    resp['success'] = True
    return resp


def create_auth_uri():
    endpoints = retrieve_endpoints();
    payload = {
        'client_id': app.config['CLIENT_ID'],
        'redirect_uri': get_redirect_uri(),
        'login': 'acbilson',
        'scope': 'user',
        'state': state,
        'allow_signup': 'false'
    }
    uri = f"{endpoints['authorization_endpoint']}?client_id={payload['client_id']}&redirect_uri={payload['redirect_uri']}&login={payload['login']}&scope={payload['scope']}&state={payload['state']}"
    return uri

def get_token(auth_code):
    endpoints = retrieve_endpoints();
    headers = {'Accept': 'application/json'}
    payload = {
            'client_id': app.config['CLIENT_ID'],
            'client_secret': app.config['CLIENT_SECRET'],
            'code': auth_code,
            'redirect_uri': get_redirect_uri(),
            'state': state,
            }
    uri = f"{endpoints['token_endpoint']}?client_id={payload['client_id']}&client_secret={payload['client_secret']}&code={payload['code']}&redirect_uri={payload['redirect_uri']}&state={payload['state']}"
    response = requests.post(uri, data=payload, headers=headers)
    data = response.json()
    return data['access_token']

def get_user_uri(token):
    headers = {
            'Authorization': f"Bearer {token}"
            }
    response = requests.post('https://api.github.com/user', headers=headers)
    return response.json()['blog']

def get_redirect_uri():
    return f"{app.config['ME']}{url_for('auth_bp.callback')}"

def retrieve_endpoints():
    return {
            'authorization_endpoint': 'https://github.com/login/oauth/authorize',
            'token_endpoint': "https://github.com/login/oauth/access_token",
            'micropub_endpoint': "https://pub.alexbilson.dev/micropub"
            }

if __name__ == '__main__':
    app.run()
