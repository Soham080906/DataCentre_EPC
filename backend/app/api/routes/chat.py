from fastapi import APIRouter
router = APIRouter(prefix="/chat", tags=["RAG Chat"])
@router.get("/history")
def get_chat_history():
    return {"history": []}
