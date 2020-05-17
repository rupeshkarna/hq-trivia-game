class CustomResponse(dict):
    def __init__(self, message, success=True):
        dict.__init__(self, message=message, success=success)
