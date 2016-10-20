# Copyright 2015 INFN
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
SSO FLASK Application for Discourse
The configuration file is defined with the variable "DISCOURSE_SSO_CONFIG",
for the most significant values look at the sso/default.py file
"""

from flask import abort, Flask, redirect, request, url_for, session
from flask_pyoidc.flask_pyoidc import OIDCAuthentication

import os
import base64
import hashlib
import hmac
import requests
from urllib.parse import quote

# Disable SSL certificate verification warning
requests.packages.urllib3.disable_warnings()

app = Flask(__name__)

# Load configuration
app.config.from_object('discourseOIDC.default.Config')

if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))

app.config.from_envvar('DISCOURSE_SSO_CONFIG', True)

# Initialize OpenID Connect extension
auth = OIDCAuthentication(app,
                          issuer=app.config['OIDC_ISSUER'],
                          client_registration_info=app.config['OIDC_CLIENT_CONFIG'])


@app.route('/')
def index():
    return redirect(app.config.get('DISCOURSE_URL'), 302)


@app.route('/sso/login')
def payload_check():
    """
    Verify the payload and signature coming from a Discourse server and if
    correct redirect to the authentication page
    :return: The redirection page to the authentication page
    """

    # Get payload and signature from Discourse request
    payload = request.args.get('sso', '')
    signature = request.args.get('sig', '')

    if not payload or not signature:
        abort(400)

    app.logger.debug('Request to login with payload="%s" signature="%s"', payload, signature)
    app.logger.debug('Session Secret Key: %s', app.secret_key)
    app.logger.debug('SSO Secret Key: %s', app.config.get('DISCOURSE_SECRET_KEY'))

    # Calculate and compare request signature
    dig = hmac.new(app.config.get('DISCOURSE_SECRET_KEY', ''), payload, hashlib.sha256).hexdigest()
    app.logger.debug('Calculated hash: %s', dig)

    if dig != signature:
        abort(400)

    # Decode the payload and store in session
    decoded_msg = base64.b64decode(payload)
    session['nonce'] = decoded_msg

    # Redirect to authorization endpoint
    return redirect(url_for('user_auth'))


@app.route('/sso/auth')
@auth.oidc_auth
def user_auth():
    """
    Read the user attributes provided by the application server (generally
    it is apache httpd) as environment variables and create the payload to
    send to discourse
    :return: The redirection page to Discourse
    """

    # Check to make sure we have a valid session
    if 'nonce' not in session:
        abort(403)

    attribute_map = app.config.get('DISCOURSE_USER_MAP')

    # External ID
    external_id = session['userinfo'].get(attribute_map['external_id'], '')
    if not external_id:
        abort(403)

    # Display name
    name_list = []
    for name_to_map in attribute_map['name']:
        if request.environ.get(name_to_map):
            name_list.append(request.environ.get(name_to_map))
    name = ' '.join(name_list)

    # Username
    username = session['userinfo'].get(attribute_map['username'], '')
    if not username:
        username = (name.replace(' ', '') + "_" + external_id[0:4])

    # Email
    email = session['userinfo'].get(attribute_map['email'], '')
    if app.config.get('SSO_EMAIL_OVERRIDE', False):
        email = username + "@" + session['userinfo'].get('SSO_EMAIL_OVERRIDE_DOMAIN')
    if not email:
        abort(403)

    app.logger.debug('Authenticating "%s" with username "%s" and email "%s"', name, username, email)

    # Build response
    query = (session['nonce'] +
             '&name=' + name +
             '&username=' + username +
             '&email=' + quote(email) +
             '&external_id=' + external_id)
    app.logger.debug('Query string to return: %s', query)

    # Encode response
    query_b64 = base64.b64encode(query)
    app.logger.debug('Base64 query string to return: %s', query_b64)

    # Build URL-safe response
    query_urlenc = quote(query_b64)
    app.logger.debug('URLEnc query string to return: %s', query_urlenc)

    # Generate signature for response
    sig = hmac.new(app.config.get('DISCOURSE_SECRET_KEY'), query_b64, hashlib.sha256).hexdigest()
    app.logger.debug('Signature: %s', sig)

    # Build redirect URL
    redirect_url = (app.config.get('DISCOURSE_URL') +
                    '/session/sso_login?'
                    'sso=' + query_urlenc +
                    '&sig=' + sig)

    # Redirect back to Discourse
    return redirect(redirect_url)


@app.route('/logout')
@auth.oidc_logout
def logout():
    return redirect(url_for('index'), 302)
