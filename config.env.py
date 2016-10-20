import os, json

#######################
# Flask Configuration #
#######################

DEBUG = True if os.environ.get('SSO_DEBUG', 'false') == 'true' else False
IP = os.environ.get('SSO_IP', '0.0.0.0')
PORT = int(os.environ.get('SSO_PORT', '8080'))
SERVER_NAME = os.environ.get('SSO_SERVER_NAME', 'discourse-sso.csh.rit.edu')
SECRET_KEY = os.environ.get('SSO_SECRET_KEY', 'thisisntverysecure')

################################
# OpenID Connect Configuration #
################################

OIDC_ISSUER = os.environ.get('SSO_OIDC_ISSUER', 'https://sso.csh.rit.edu/realms/csh')
OIDC_CLIENT_CONFIG = {
    'client_id': os.environ.get('SSO_OIDC_CLIENT_ID', 'discourse'),
    'client_secret': os.environ.get('SSO_OIDC_CLIENT_SECRET', ''),
    'post_logout_redirect_uris': [os.environ.get('SSO_OIDC_LOGOUT_REDIRECT_URI',
                                                 'https://' + SERVER_NAME + '/logout')]
}

###########################
# Discourse Configuration #
###########################

# Discourse URL to send the user back
DISCOURSE_URL = os.environ.get('SSO_DISCOURSE_URL', 'http://discuss.example.com')

# Secret key shared with the Discourse server
DISCOURSE_SECRET_KEY = os.environ.get('SSO_DISCOURSE_SECRET', '')

# Attribute to read from the environment after user validation
DISCOURSE_USER_MAP = json.loads(os.environ.get('SSO_DISCOURSE_USER_MAP',
                                               '{"name": ["givenName", "sn"], "username": "preferred_username", \
                                               "external_id": "sub", "email": "email"}'))
