class UserBot:
    def __init__(self, client):
        """
        :param client: Telethon client class
        """
        self.client = client

    def add_func(self, func):
        """
        :param func: handler function
        """
        setattr(self.__class__, func.__name__, func)
