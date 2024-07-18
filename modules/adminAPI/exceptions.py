from fastapi import HTTPException, status


INSUFFICIENT_PERMISSIONS_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Insufficient permissions to operate"
)

RIGTHS_CONFLICT_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Conflict of rights. You try manipulate other admin"
)