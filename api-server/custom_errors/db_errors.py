class InvalidProvider(Exception):
    """Error raised when user provides an unsupported provider or when the provider entry does not exist.

    Args:
        Exception (_type_): _description_
    """
    
    def __init__(self, provider):
        self.message = f"""Invalid provider; could not find the provider: '{provider}'."""
        self.status_code = 400
        super().__init__(self.message)


class InvalidModel(Exception):
    """Error raised when user provides an unsupported model or when the model entry does not exist.

    Args:
        Exception (_type_): _description_
    """
    
    def __init__(self, model):
        self.message = f"""Invalid model; could not find the model: '{model}'."""
        self.status_code = 400 
        super().__init__(self.message)

class InvalidSecret(Exception):
    """Error raised when user provides an invalid secret ID or when the secret ID entry does not exist.

    Args:
        Exception (_type_): _description_
    """
    
    def __init__(self, secret_id):
        self.message = f"""Invalid Secret; could not find the secret with ID = '{secret_id}'."""
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
            self.message = f"""Invalid date range; there are no usages recorded from '{start_date}' to '{end_date}'."""
        self.status_code = 400
        super().__init__(self.message)