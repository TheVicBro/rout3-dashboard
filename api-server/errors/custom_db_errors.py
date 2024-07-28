class InvalidProvider(Exception):
    """Error raised when user provides an unsupported provider

    Args:
        Exception (_type_): _description_
    """
    
    def __init__(self, provider):
        self.message = f"""The provider: '{provider}' is not supported."""
        self.status_code = 400
        super().__init__(self.message)


class InvalidModel(Exception):
    """Error raised when user provides an unsupported model

    Args:
        Exception (_type_): _description_
    """
    
    def __init__(self, model):
        self.message = f"""The model: '{model}' is not supported."""
        self.status_code = 400 
        super().__init__(self.message)

class InvalidSecret(Exception):
    """Error raised when user provides an invalid secret

    Args:
        Exception (_type_): _description_
    """
    
    def __init__(self, secret_id):
        self.message = f"""The secret with id = '{secret_id}', does not exist."""
        self.status_code = 400
        super().__init__(self.message)
        

class InvalidDateRangeUsage(Exception):
    """Error raised when user provides a date range that has no usages recorded

    Args:
        Exception (_type_): _description_
    """
    def __init__(self, start_date, end_date):
        if start_date > end_date:
            self.message = "Invalid date range; start_date is more recent than end_date."
        else: 
            self.message = f"""There are no usages recorded from '{start_date}' to '{end_date}'."""
        self.status_code = 400
        super().__init__(self.message)