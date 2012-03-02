#!/usr/bin/env python

import socket

__author__ = 'Shawn McTear'
__version__ = '0.1.0'

class PySNP(object):
    host = '127.0.0.1'
    port = 9887

    def __init__(self, **address):
        """Creates an object of pySNP."""
        if 'host' in address:
            self.host = address['host']
        if 'port' in address:
            self.port = address['port']

    def _send(self, request, errors):
        """Trys to sends the request to Snarl"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.host, self.port))
            self.sock.send((request + '\r\n').encode("UTF-8"))
            recv = str(self.sock.recv(1024),"UTF-8").rstrip('\r\n')
            self.sock.close()
            self._response(recv, errors, request)
        except IOError:
            errors = self._error(1, 'noserver', None, None)
            self._error(2, None, errors, None)

    def _response(self, recv, errors, request):
        """Displays Snarl's response"""
        self._error(2, None, errors, None)
        
    def _process(self, action, data, args):
        """Processes everything from the actions"""
        errors = self._error()
        request = 'snp://' + action
        param = ''

        # Fills data with info from args if needed
        for val in data:
            if val in args:
                data[val][2] = args[val]

        # Checks if data is required and if vals are empty
        for key, val in sorted(list(data.items()), key=lambda x: x[1]):
            if val[1] is True and val[2]:
                param = param + '&' + key + '=' + val[2]
            elif val[1] is True and not val[2]:
                errors = self._error(1, 'missing', errors, key)
            elif val[1] is False and val[2]:
                param = param + '&' + key + '=' + val[2]
            else:
                pass

        # Checks for errors before sending
        if not errors:
            param = param.replace('&', '?', 1)
            request = request + param
        self._send(request, errors)

    def _error(self, mode=0, issue=None, errors=None, obj=None):
        """Assigns and displays errors"""
        issue = issue or ''
        errors = errors or []
        obj = obj or ''

        if mode is 1 and issue is 'missing':
            error = "*Error: '%s' is missing.*" % obj
            errors.append(error)
        elif mode is 1 and issue is 'noserver':
            error = "*Error: Can't connect to Snarl.*"
            errors.append(error)
        elif mode is 2:
            for error in errors:
                print(error)
        else:
            pass
        return errors

    def register(self, app_sig='', app_title='', **args):
        """Snarl's register action"""
        action = 'register'
        data = {'app-sig': [1, True, app_sig],
                'password': [2, False, ''],
                'title': [3, True, app_title],
                'icon': [4, False, '']}
        self._process(action, data, args)

    def notify(self, app_sig='', title='', text='', **args):
        """Snarl's notify action"""
        action = 'notify'
        data = {'app-sig': [1, True, app_sig],
                'password': [2, False, ''],
                'title': [3, True, title],
                'text': [4, False, text],
                'icon': [5, False, ''],
                'id': [6, False, ''],
                'uid': [7, False, ''],
                'timeout': [8, False, ''],
                'priority': [9, False, '']}
        self._process(action, data, args)

    def addclass(self, app_sig='', cid='', cname='', **args):
        """Snarl's addclass action"""
        action = 'addclass'
        data = {'app-sig': [1, True, app_sig],
                'password': [2, False, ''],
                'title': [3, False, ''],
                'text': [4, False, ''],
                'icon': [5, False, ''],
                'id': [6, True, cid],
                'name': [7, True, cname],
                'enabled': [8, False, '']}
        self._process(action, data, args)

    def version(self, **args):
        """Snarl's version action"""
        action = 'version'
        data = {}
        self._process(action, data, args)

    def unregister(self, app_sig='', **args):
        """Snarl's unregister action"""
        action = 'unregister'
        data = {'app-sig': [1, True, app_sig],
                'password': [2, False, '']}
        self._process(action, data, args)
        