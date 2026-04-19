from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

from schema import MachineInput, ChatRequest, ChatResponse
from predictor import predict_machine_failure
from vehiclereport import generate_maintenance_report
from rag_service import get_chat_response



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "running Welcome to Machine Failure Prediction API"}    

@app.post("/predict")
async def predict(data: MachineInput):
    try:
      
        prediction_result = predict_machine_failure(data.dict())
        
       
        vehicle_type = 'L' if data.Type_L else 'M'
        
       
        detailed_report = await generate_maintenance_report(
            prediction_result=prediction_result,
            vehicle_type=vehicle_type,
            vehicle_age=data.machine_age,
            total_kilometers=data.total_kilometers,
            vehicle_name=data.vehicle_name,
            model=data.model
        )
        
       
        return {
            "report": detailed_report,
            "prediction": prediction_result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Convert history format for the service
        history_list = [{"role": m.role, "content": m.content} for m in request.history]
        
        chat_data = await get_chat_response(request.message, history_list)
        
        return ChatResponse(
            response=chat_data["response"],
            sources=chat_data.get("sources")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
