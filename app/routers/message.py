from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.message import MessageCreate, MessageResponse
from app.models.message import Message
from app.models.user import User
from app.models.conversation import Conversation
from app.models.notification import Notification
from app.database.connection import get_db
from app.services.translation_service import translate_message

router = APIRouter(
    prefix="/messages",
    tags=["messages"]
)

@router.post("/send", response_model=MessageResponse)
def send_message(message_data: MessageCreate, db: Session = Depends(get_db)):
    # Verificar que la conversación esté aceptada antes de enviar mensajes
    conversation = db.query(Conversation).filter(
        (Conversation.id == message_data.conversation_id) &
        (Conversation.accepted == True)
    ).first()

    if not conversation:
        raise HTTPException(status_code=400, detail="Conversation not accepted")

    # Determinar el receptor en la conversación
    receiver_id = conversation.user1_id if message_data.sender_id == conversation.user2_id else conversation.user2_id
    receiver = db.query(User).filter(User.id == receiver_id).first()

    # Crear el mensaje con traducción si el receptor tiene auto_translate activado
    translated_content = None
    if receiver and receiver.auto_translate:
        translated_content = translate_message(message_data.content, "es")  # Traduce al idioma deseado, aquí "es" para español

    # Crear el mensaje con el contenido original y traducido
    message = Message(
        conversation_id=message_data.conversation_id,
        sender_id=message_data.sender_id,
        content=message_data.content,
        translated_content=translated_content
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    
        # Crear notificación para el receptor
    notification = Notification(
        user_id=receiver_id,
        message_id=message.id
    )
    db.add(notification)
    db.commit()
    return message

@router.get("/{conversation_id}", response_model=list[MessageResponse])
def get_messages(conversation_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.timestamp).all()
    return messages

@router.put("/{message_id}/read", response_model=MessageResponse)
def mark_message_as_read(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    message.read = True
    db.commit()
    db.refresh(message)
    return message
