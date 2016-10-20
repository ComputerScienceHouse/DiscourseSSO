OpenID Connect for Discourse
============================

[![Travis-CI Build Status](http://img.shields.io/travis/fmarco76/DiscourseSSO/master.png?style=flat)](https://travis-ci.org/fmarco76/DiscourseSSO) [![Coverage Status](https://coveralls.io/repos/fmarco76/DiscourseSSO/badge.svg?style=flat)](https://coveralls.io/r/fmarco76/DiscourseSSO) [![Code Quality Status](https://landscape.io/github/fmarco76/DiscourseSSO/master/landscape.svg?style=flat)](https://landscape.io/github/fmarco76/DiscourseSSO/master) [![Codacy Status](https://www.codacy.com/project/badge/ff8b39c8455d4f2ca4ead7e034f6b6d6)](https://www.codacy.com/app/marco-fargetta/DiscourseSSO) [![License](https://img.shields.io/badge/license-Apache%202-blue.svg)](LICENSE)

This application implements the SSO protocol requested by the [Discourse forum application]. The real authentication is performed by an OpenID Connect IdP configured in this app which is responsible for verifying the requests coming from Discourse and prepare the token to send back after authentication.

Based on [fmarco76's DiscourseSSO].

Installation
------------

Both Discourse and DiscourseSSO need to be configured. Enable SSO in Discourse following the [official documentation]. The SSO url to is the one going to your DiscourseSSO installation plus `sso/login`. For example: `https://<your-domain>/sso/login`.

The sso\_secret is a random string and has to be the same in both services. The configuration file of DiscourseSSO is `config.py` and it require the secret key (`DISCOURSE_SECRET_KEY`), the url of Discourse (`DISCOURSE_URL`), OpenID Connect IdP configuration info, among other general environment settings. There is also a map where the key is the attribute provided back to Discourse whereas the values are the name of the variables in the OpenID Connect userdata info to lookup. The name can be generated combining different values but the other accept only one value.

  [Discourse forum application]: http://www.discourse.org
  [official documentation]: https://meta.discourse.org/t/official-single-sign-on-for-discourse/13045
  [fmarco76's DiscourseSSO]: https://github.com/fmarco76/DiscourseSSO