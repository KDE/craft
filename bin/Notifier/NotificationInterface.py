class NotificationInterface(object):
    def __init__(self, name):
        self.name = name
        
    def notify(self,title,message):
        raise NameError('Not Implemented')
        
