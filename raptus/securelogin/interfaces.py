# -*- coding: utf-8 -*-
from zope import interface
from zope import schema

from raptus.securelogin import SecureLoginMessageFactory as _


class IConfiguration(interface.Interface):

    ip_bypass = schema.List(
        title=_(u'IP'),
        description=_(u'IPs for which to bypass the secure login procedure.'),
        required=False,
        value_type=schema.TextLine()
    )

    groups = schema.Set(
        title=_(u'Groups'),
        description=_(u'Groups for which to enforce the secure login procedure.'),
        value_type=schema.Choice(
            source='plone.app.vocabularies.Groups',
        ),
        required=False
    )

    email = schema.TextLine(
        title=_(u'Email pattern'),
        description=_(u'The email address (has to contain «%(number)s;», which will'
                       'be replaced by the mobile phone number of the user) to send'
                       'the security token to.'),
        required=True
    )

    timeout = schema.Int(
        title=_(u'Timeout'),
        description=_(u'Number of seconds a security token is valid.'),
        default=300,
        required=True
    )


class ISecure(interface.Interface):

    def enabled(username):
        """ Whether secure login is enabled for the provided user
        """

    def has_token(username):
        """ Whether the provided user already received a token
        """

    def check(username, token):
        """ Whether the given token is correct for the provided user
        """

    def send(username):
        """ Send a new security token to the provided user
        """
