from fastapi import APIRouter, FastAPI, HTTPException
from app.models.Req_Res_schemas import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Here you would integrate with your LLM service to get the response
        # For demonstration, we will return a dummy response
        response = ChatResponse(
            natural_language_answer="This is a dummy answer.",
            sql_query="SELECT * FROM inventory;",
            token_usage={"input_tokens": 10, "output_tokens": 5},
            latency_ms=100.0,
            provider="DummyProvider",
            model="DummyModel",
            status="success"
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))