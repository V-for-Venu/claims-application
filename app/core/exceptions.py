from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse


class FastClaimsError(Exception):
    """Base Exception for All Exceptions in FastClaims API"""


class EntityNotFoundError(FastClaimsError):
    """Entity not found in the Database"""

    status = status.HTTP_404_NOT_FOUND


class InvalidCredentials(FastClaimsError):
    """Invalid Credentials, Please provider Valid Credentials"""

    status = status.HTTP_401_UNAUTHORIZED


class InvalidTokenError(FastClaimsError):
    """Invalid Token, Please enter a valid JWT Token"""

    status = status.HTTP_401_UNAUTHORIZED


class ExpiredTokenError(FastClaimsError):
    """Authorization Failed due to Token Expiry, Please Login Again"""

    status = status.HTTP_401_UNAUTHORIZED


class AuthorizationError(FastClaimsError):
    """Unauthorized Data Access is Restricted."""

    status = status.HTTP_401_UNAUTHORIZED


class InvalidRequestError(FastClaimsError):
    """Invalid Request, Please enter a Valid Request"""

    status = status.HTTP_400_BAD_REQUEST


def _get_handler(status: int, detail: str):
    def handler(request: Request, exception: Exception) -> Response:
        from rich import panel, print

        print(
            panel.Panel(
                f"Handled {exception.__class__.__name__}", border_style="bright_yellow"
            )
        )
        raise HTTPException(
            detail={"message": detail},
            status_code=status,
        )

    return handler


def add_exception_handler(app: FastAPI):
    for subclass in FastClaimsError.__subclasses__():
        app.add_exception_handler(
            subclass, _get_handler(subclass.status, subclass.__doc__)
        )

    @app.exception_handler(ResponseValidationError)
    def response_validation_error_handler(request, exception):
        error_msg = exception.errors()[0]["msg"]
        return JSONResponse(
            content={"error": "Something Went Wrong..."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            headers={"X-Error": error_msg},
        )

    @app.exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR)
    def internal_server_error_handler(request, exception):
        return JSONResponse(
            content={"error": "Something Went Wrong..."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            headers={"X-Error": f"{exception}"},
        )
