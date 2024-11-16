from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.conversation import ConversationResponse, ConversationCreate
from app.models.conversation import Conversation
from app.database.connection import get_db

router = APIRouter(
    prefix="/conversations",
    tags=["conversations"]
)

@router.post("/request", response_model=ConversationResponse)
def request_conversation(conversation_data: ConversationCreate, db: Session = Depends(get_db)):
    # Verificar si la conversación ya existe entre los usuarios
    existing_conversation = db.query(Conversation).filter(
        ((Conversation.user1_id == conversation_data.user1_id) & (Conversation.user2_id == conversation_data.user2_id)) |
        ((Conversation.user1_id == conversation_data.user2_id) & (Conversation.user1_id == conversation_data.user1_id))
    ).first()

    if existing_conversation:
        raise HTTPException(status_code=400, detail="Conversation already exists")

    # Crear la solicitud de conversación
    conversation = Conversation(**conversation_data.dict())
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

@router.put("/{conversation_id}/accept", response_model=ConversationResponse)
def accept_conversation(conversation_id: int, db: Session = Depends(get_db)):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Actualizar el estado de aceptación
    conversation.accepted = True
    db.commit()
    db.refresh(conversation)
    return conversation

@router.get("/{conversation_id}", response_model=ConversationResponse)
def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.get("/user/{user_id}", response_model=list[ConversationResponse])
def get_user_conversations(user_id: int, db: Session = Depends(get_db)):
    conversations = db.query(Conversation).filter(
        (Conversation.user1_id == user_id) | (Conversation.user2_id == user_id)
    ).all()
    return conversations
