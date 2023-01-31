from pydantic import BaseModel


class ResetPassword(BaseModel):
    email: str
    # new_password: str
