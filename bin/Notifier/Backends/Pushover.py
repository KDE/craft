from Notifier.NotificationInterface import *
from CraftConfig import *

class Pushover(NotificationInterface):
    def __init__(self):
        NotificationInterface.__init__(self,'Pushover')
        
    def notify(self,title,message,alertClass):
        import os
        import http.client
        import urllib
        
        app_token = craftSettings.get('General', 'EMERGE_PUSHOVER_APP_TOKEN', 'aJU9PRUb6nGUUM2idyLfXdU8S5q18i')
        user_key = craftSettings.get('General', 'EMERGE_PUSHOVER_USER_KEY')
        
        if user_key == None:
            return
        try:
            conn = http.client.HTTPSConnection('api.pushover.net:443')
            conn.request('POST', '/1/messages.json',
                urllib.parse.urlencode({'token': app_token, 'user': user_key, 'title': title, 'message': message, }),
                    { 'Content-type': 'application/x-www-form-urlencoded' }
            )
        except Exception:
        	return
