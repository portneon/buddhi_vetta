from pydantic import BaseModel, Field
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = Field(default_factory=list)

class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[str]] = None

class MachineInput(BaseModel):
    Air_temperature: float
    Process_temperature: float
    Rotational_speed: float
    Torque: float
    Tool_wear: float
    Type_L: bool = Field(default=False, description="Low quality machine type")
    Type_M: bool = Field(default=True, description="Medium quality machine type")
    vehicle_name: str = Field(default="Unknown", description="Vehicle name or ID")
    model: str = Field(default="Unknown", description="Vehicle model")
    machine_age: float = Field(default=0, description="Vehicle age in years")
    total_kilometers: float = Field(default=0, description="Total kilometers traveled")
