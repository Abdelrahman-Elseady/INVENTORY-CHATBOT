from fastapi import APIRouter, FastAPI, HTTPException
from app.models.Req_Res_schemas import ChatRequest, ChatResponse
from app.services.chat_service import handle_chat
from app.db.validator import validate_sql
from app.core.config import settings

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        result = handle_chat(request.user_message)

        if not validate_sql(result["sql"]):
            raise HTTPException(status_code=400, detail="Unsafe SQL detected")

        return ChatResponse(
            natural_language_answer=result["answer"],
            sql_query=result["sql"],
            token_usage=result["token_usage"],
            latency_ms=result["latency"],
            provider=settings.PROVIDER,
            model=settings.MODEL_NAME,
            status="ok"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))