class IcesException(Exception):
    def __init__(self, message):
        self.message = message
        super(IcesException, self).__init__(message)
