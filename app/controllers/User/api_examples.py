from app.responses.ErrorResponse import ErrorResponse

login_example = {
    "example": {
        "summary": "Login user endpoint",
        "description": "An example of user login request",
        "value": {
            "username": "funkymonkey123",
            "password": "123456",
        },
    },
}

register_example = {
    "example": {
        "summary": "Register user endpoint",
        "description": "An example of register login request",
        "value": {
            "first_name": "Tomas",
            "last_name": "Svojanovsky",
            "username": "testname",
            "email": "tomas.svojanovsky11@gmail.com",
            "birthdate": "1991-01-01",
            "password": "123456"
        },
    },
}

register_error_responses = {
    409: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
}


change_password_example = {
    "example": {
        "summary": "Change password user endpoint",
        "description": "An example of change password request",
        "value": {
            "old_password": "123456",
            "new_password": "1234567",
        },
    },
}
