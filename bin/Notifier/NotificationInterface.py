class NotificationInterface(object):
    def __init__(self, name):
        self.name = name
        
    def notify(self,title,message,alertClass):
        raise NameError('Not Implemented')
        
