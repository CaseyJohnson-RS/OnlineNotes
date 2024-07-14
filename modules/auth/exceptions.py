from fastapi import HTTPException, status

UNAUTHORIZED_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

CREDENTIALS_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

INACTIVE_USER_EXCEPTION = HTTPException(
    status_code=400, 
    detail="Inactive user"
)

USERNAME_EXISTS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, 
    detail="Username already exists"
)

LATE_CONFIRM_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, 
    detail="Confirmation is too late"
)

BAD_CONFIRMATION_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The user was not in the registration confirmation buffer"
)

WRONG_CONFIRMATION_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Confirmation sequence is wrong"
)