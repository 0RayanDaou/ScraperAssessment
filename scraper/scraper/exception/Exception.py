# Define the custom exception class
class MultipleMatches(Exception):
    def __init__(self, message):
        # Call the base class constructor with the custom message
        super().__init__(message)

class ValueError(Exception):
    def __init__(self, message):
        super().__init__(message)

class LoopException(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidObjectType(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidOperation(Exception):
    def __init__(self, message):
        super().__init__(message)