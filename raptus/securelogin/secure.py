from hashlib import sha256
from time import time

from zope import interface
from zope import component
from zope.site.hooks import getSite
from zope.publisher.interfaces import IRequest

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

from raptus.securelogin import interfaces

import logging

TOKEN_KEY = 'raptus.securelogin.token'
VALID_KEY = 'raptus.securelogin.valid'


class Secure(object):

    interface.implements(interfaces.ISecure)
    component.adapts(interface.Interface, IRequest)

    def __init__(self, context, request):
        self.request = request
        self.context = getSite()
        self.configuration = interfaces.IConfiguration(getSite())
        self.membership = getToolByName(self.context, 'portal_membership')
        self.registration = getToolByName(self.context, 'portal_registration')

    def _hash(self, token):
        hash = sha256()
        hash.update(token + str(int(time() / self.configuration.timeout)))
        return hash.digest()

    def enabled(self, username):
        """ Whether secure login is enabled for the provided user
        """
        return True

    def has_token(self, username):
        """ Whether the provided user already received a token
        """
        return self.request.SESSION.get(VALID_KEY + '.' + username, False) == self._hash('')

    def check(self, username, token):
        """ Whether the given token is correct for the provided user
        """
        if self._hash(token) == self.request.SESSION.get(TOKEN_KEY + '.' + username, False):
            self.request.SESSION.set(TOKEN_KEY + '.' + username, False)
            return True
        return False

    def send(self, username):
        """ Send a new security token to the provided user
        """
        token = self.registration.getPassword(8)
        self.request.SESSION.set(TOKEN_KEY + '.' + username, self._hash(token))
        self.request.SESSION.set(VALID_KEY + '.' + username, self._hash(''))
        logging.info(token)
