from pydantic import BaseModel
import asyncpg


class ApiKey(BaseModel):
    id: int
    user_id: int
    api_key: str

    @classmethod
    def from_db(cls, row: asyncpg.Record):
        return cls(id=row["id"], user_id=row["user_id"], api_key=row["api_key"])

