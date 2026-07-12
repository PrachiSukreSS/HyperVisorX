from pydantic import BaseModel

class VirtualMachineResponse(BaseModel):
    name: str
    id: int
    state: str