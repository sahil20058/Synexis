from pydantic import BaseModel

class ActionRequest(BaseModel):
    action: str

class ResetRequest(BaseModel):
    task: str