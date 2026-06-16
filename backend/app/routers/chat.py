from fastapi import APIRouter, Depends, HTTPException

from app.models.schemas import ChatRequest, ChatResponse
from app.services.llm_service import LLMService
from app.services.user_state import UserStateManager

router = APIRouter(prefix="/chat", tags=["chat"])


def get_llm() -> LLMService:
    return LLMService()


def get_state() -> UserStateManager:
    return UserStateManager()


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    llm: LLMService = Depends(get_llm),
    state: UserStateManager = Depends(get_state),
):
    user = state.get_user(request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    response = await llm.generate(
        feature=request.feature,
        user_input=request.message,
        user_context=user,
    )

    state.add_to_history(request.user_id, request.message, response)

    return ChatResponse(
        message=response.content,
        structured_data=response.structured_data,
    )
