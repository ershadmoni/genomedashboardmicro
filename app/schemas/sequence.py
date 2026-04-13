from pydantic import BaseModel


class SequenceRequest(BaseModel):
    sequence: str
