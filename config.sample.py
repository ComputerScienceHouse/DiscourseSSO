#######################
# Flask Configuration #
#######################

DEBUG = False
IP = '0.0.0.0'
PORT = 8080
SERVER_NAME = localhost:8080
SECRET_KEY = 'thisisntverysecure'

################################
# OpenID Connect Configuration #
################################

OIDC_ISSUER = 'https://sso.csh.rit.edu/realms/csh'
OIDC_CLIENT_CONFIG = {
    'client_id': 'discourse',
    'client_secret': '',
    'post_logout_redirect_uris': ['https://' + SERVER_NAME + '/logout']
}

###########################
# Discourse Configuration #
###########################

# Discourse URL to send the user back
DISCOURSE_URL = 'http://discuss.example.com'

# Secret key shared with the Discourse server
DISCOURSE_SECRET_KEY = ''

# Attribute to read from the environment after user validation
DISCOURSE_USER_MAP = {
    "name": ["givenName", "sn"],
    "username": "preferred_username",
    "external_id": "sub",
    "email": "email"
}