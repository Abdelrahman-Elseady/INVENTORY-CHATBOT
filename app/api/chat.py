from fastapi import APIRouter, FastAPI, HTTPException
from app.models.Req_Res_schemas import ChatRequest, ChatResponse
from app.services.chat_service import generate_sql_response

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        response = generate_sql_response(request.user_message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))