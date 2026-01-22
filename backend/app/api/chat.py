"""
Chat API Endpoint for AI Todo Assistant
Implements stateless chat with conversation persistence
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlmodel import Session, select
import logging
import uuid
from ..core.database import get_session
from ..models.models import Conversation, Message
from ..agent import run_agent

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s | request_id=%(request_id)s | %(message)s'
)

router = APIRouter(prefix="/api", tags=["chat"])

class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str = Field(..., min_length=1, max_length=2000)
    
    @validator('message')
    def validate_message(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty or whitespace only')
        return v.strip()

class ErrorResponse(BaseModel):
    status: str = "error"
    code: str
    message: str
    recoverable: bool
    request_id: str

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[Dict[str, Any]]
    request_id: str

@router.post("/{user_id}/chat", response_model=ChatResponse, responses={
    400: {"model": ErrorResponse, "description": "Invalid request"},
    404: {"model": ErrorResponse, "description": "Conversation not found"},
    500: {"model": ErrorResponse, "description": "Server error"}
})
async def chat(
    user_id: str,
    request: ChatRequest,
    session: Session = Depends(get_session)
):
    """
    Stateless chat endpoint for AI todo assistant
    
    Flow:
    1. Validate inputs
    2. Get/create conversation
    3. Fetch conversation history from DB
    4. Store user message in DB
    5. Run agent with MCP tools (with error boundaries)
    6. Store assistant response in DB
    7. Return response to client
    """
    # Generate request ID for tracing
    request_id = str(uuid.uuid4())
    logger.info(f"Chat request started", extra={"request_id": request_id})
    
    # Step 1: Input validation
    if not user_id or not user_id.strip():
        logger.error("Missing user_id", extra={"request_id": request_id})
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "code": "MISSING_USER_ID",
                "message": "user_id is required",
                "recoverable": True,
                "request_id": request_id
            }
        )
    
    try:
        # Step 2: Get or create conversation
        if request.conversation_id:
            conversation = session.get(Conversation, request.conversation_id)
            if not conversation:
                logger.warning(
                    f"Conversation {request.conversation_id} not found",
                    extra={"request_id": request_id}
                )
                raise HTTPException(
                    status_code=404,
                    detail={
                        "status": "error",
                        "code": "CONVERSATION_NOT_FOUND",
                        "message": f"Conversation {request.conversation_id} does not exist",
                        "recoverable": True,
                        "request_id": request_id
                    }
                )
            
            if conversation.user_id != user_id:
                logger.warning(
                    f"User {user_id} attempted to access conversation {request.conversation_id} owned by {conversation.user_id}",
                    extra={"request_id": request_id}
                )
                raise HTTPException(
                    status_code=403,
                    detail={
                        "status": "error",
                        "code": "UNAUTHORIZED_CONVERSATION",
                        "message": "You don't have access to this conversation",
                        "recoverable": False,
                        "request_id": request_id
                    }
                )
            
            # Update conversation timestamp
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
        else:
            # Create new conversation
            conversation = Conversation(user_id=user_id)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            logger.info(
                f"Created new conversation {conversation.id}",
                extra={"request_id": request_id}
            )
        
        # Step 3: Fetch conversation history
        statement = select(Message).where(
            Message.conversation_id == conversation.id
        ).order_by(Message.created_at)
        
        history_messages = session.exec(statement).all()
        
        # Build message array for agent
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in history_messages
        ]
        
        # Add new user message
        messages.append({"role": "user", "content": request.message})
        
        logger.info(
            f"Loaded {len(history_messages)} history messages",
            extra={"request_id": request_id}
        )
        
        # Step 4: Store user message in DB
        user_message = Message(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content=request.message
        )
        session.add(user_message)
        session.commit()
        
        # Step 5: Run agent with error boundaries
        try:
            logger.info("Starting agent execution", extra={"request_id": request_id})
            agent_result = await run_agent(messages, user_id)
            logger.info(
                f"Agent execution completed with {len(agent_result.get('tool_calls', []))} tool calls",
                extra={"request_id": request_id}
            )
        except Exception as agent_error:
            logger.exception(
                f"Agent execution failed: {str(agent_error)}",
                extra={"request_id": request_id}
            )
            raise HTTPException(
                status_code=500,
                detail={
                    "status": "error",
                    "code": "AGENT_EXECUTION_FAILED",
                    "message": f"AI agent encountered an error: {str(agent_error)}",
                    "recoverable": True,
                    "request_id": request_id
                }
            )
        
        # Validate agent response
        if not agent_result.get("response"):
            logger.error(
                "Agent returned empty response",
                extra={"request_id": request_id}
            )
            raise HTTPException(
                status_code=500,
                detail={
                    "status": "error",
                    "code": "EMPTY_AGENT_RESPONSE",
                    "message": "AI agent returned an empty response",
                    "recoverable": True,
                    "request_id": request_id
                }
            )
        
        # Step 6: Store assistant response in DB
        assistant_message = Message(
            conversation_id=conversation.id,
            user_id=user_id,
            role="assistant",
            content=agent_result["response"]
        )
        session.add(assistant_message)
        session.commit()
        
        logger.info("Chat request completed successfully", extra={"request_id": request_id})
        
        # Step 7: Return response to client
        return ChatResponse(
            conversation_id=conversation.id,
            response=agent_result["response"],
            tool_calls=agent_result.get("tool_calls", []),
            request_id=request_id
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions (already logged)
        raise
    except Exception as e:
        # Catch-all for unexpected errors
        logger.exception(
            f"Unexpected error in chat endpoint: {str(e)}",
            extra={"request_id": request_id}
        )
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred. Please try again.",
                "recoverable": True,
                "request_id": request_id
            }
        )

