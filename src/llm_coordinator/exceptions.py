class CoordinatorError(Exception):
    """ Base exception """
    def __init__(self, message: str, status_code: int | None = None, is_retryable: bool = False) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.is_retryable = is_retryable


class TransientError(CoordinatorError):
    """ Exception for transient errors """
    def __init__(self, message: str, status_code: int | None = None, cause: str | None = None) -> None:
        super().__init__(message, status_code=status_code, is_retryable=True)
        self.cause = cause


class RateLimitError(TransientError):
    """ Exception for rate limit errors """
    def __init__(self, message: str = "Rate limit exceeded", retry_after: float | None = None) -> None:
        super().__init__(message, status_code=429  )
        self.retry_after = retry_after # non posso passarlo a TransientError, attributo solo in questa classe


class ProviderTimeoutError(TransientError):
    """ Exception for provider timeout """
    def __init__(self, message: str = "Provider timeout", timeout: float | None = None) -> None:
        super().__init__(message, status_code=504)
        self.timeout = timeout


class ServerUnavailableProviderError(TransientError):
    """ Exception for server unavailable provider errors """
    def __init__(self, message: str = "Server unavailable provider", cause: str | None = None) -> None:
        super().__init__(message, status_code=503)
        self.cause = cause


# permanent errors
class PermanentError(CoordinatorError):
    """ Exception for permanent errors """
    def __init__(self, message: str, status_code: int | None = None, cause: str | None = None) -> None:
        super().__init__(message, status_code=status_code)
        self.cause = cause


class InvalidRequestError(PermanentError):
    """ Exception for invalid requests """
    def __init__(self, message: str = "Invalid request error", cause: str | None = None) -> None:
        super().__init__(message, status_code=400)
        self.cause = cause


class ProviderNotFoundError(PermanentError):
    """ Exception for LLM provider not registered """
    def __init__(self, message: str = "Provider unknown", cause: str | None = None) -> None:
        super().__init__(message, status_code=404)
        self.cause = cause


class AuthError(PermanentError):    
    """ Exception for Auth invalid """
    def __init__(self, message: str = "Auth failed", cause: str | None = None) -> None:
        super().__init__(message, status_code=401) #work done from father class PermanentError, where cause = None then; for CoordinatorError status_code 401
        self.cause = cause #value in the instance from code   
