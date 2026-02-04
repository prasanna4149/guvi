from fastapi import APIRouter, Depends, HTTPException
from app.api.schemas import MessageRequest, MessageResponse
from app.core.security import get_api_key
from app.agent.controller import AgentController
from app.reporting.response_builder import ResponseBuilder
from app.extraction.extractor import IntelExtractor
from app.memory.store import memory_store

router = APIRouter()
controller = AgentController()

@router.post("/message", response_model=MessageResponse)
async def handle_message(
    request: MessageRequest
):
    try:
        # 1. Processing via Agent Controller
        reply, meta = await controller.process_turn(request.conversation_id, request.message)
        
        # 2. Side-effect: Extract Intel (could be inside controller, but keeping separate for cleanliness)
        new_intel = IntelExtractor.extract(request.message, meta.get("turn", 0))
        if new_intel:
            state = await memory_store.get_conversation(request.conversation_id)
            if state:
                state.extracted_data.extend(new_intel)
                meta["new_intel"] = len(new_intel)
                meta["all_intel"] = [i.model_dump() for i in state.extracted_data]
                await memory_store.save_conversation(state)

        # 3. Build Response
        return ResponseBuilder.build(request.conversation_id, reply, meta)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
