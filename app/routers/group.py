from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.group import GroupCreate, GroupResponse
from app.schemas.group_message import GroupMessageCreate, GroupMessageResponse
from app.models.group import Group
from app.models.group_member import GroupMember
from app.models.group_message import GroupMessage
from app.models.notification import Notification
from app.models.user import User
from app.database.connection import get_db
from datetime import datetime

router = APIRouter(
    prefix="/groups",
    tags=["groups"]
)

# Endpoint para crear un grupo
@router.post("/", response_model=GroupResponse)
def create_group(group_data: GroupCreate, db: Session = Depends(get_db)):
    # Crear el grupo
    group = Group(name=group_data.name)
    db.add(group)
    db.commit()
    db.refresh(group)

    # Agregar miembros al grupo
    for user_id in group_data.member_ids:
        group_member = GroupMember(group_id=group.id, user_id=user_id)
        db.add(group_member)

    db.commit()
    return group

# Endpoint para agregar un miembro al grupo
@router.post("/{group_id}/add-member")
def add_member_to_group(group_id: int, user_id: int, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    # Verificar si el usuario ya es miembro
    existing_member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == user_id
    ).first()

    if existing_member:
        raise HTTPException(status_code=400, detail="User is already a member of the group")

    # Agregar nuevo miembro
    new_member = GroupMember(group_id=group_id, user_id=user_id)
    db.add(new_member)
    db.commit()
    return {"message": "Member added successfully"}

# Endpoint para eliminar un miembro del grupo
@router.delete("/{group_id}/remove-member")
def remove_member_from_group(group_id: int, user_id: int, db: Session = Depends(get_db)):
    group_member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == user_id
    ).first()

    if not group_member:
        raise HTTPException(status_code=404, detail="Member not found in group")

    db.delete(group_member)
    db.commit()
    return {"message": "Member removed successfully"}

# Endpoint para enviar un mensaje en un grupo
@router.post("/{group_id}/send-message", response_model=GroupMessageResponse)
def send_group_message(group_id: int, message_data: GroupMessageCreate, db: Session = Depends(get_db)):
    # Verificar que el grupo existe
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    # Crear el mensaje en el grupo
    group_message = GroupMessage(
        group_id=group_id,
        sender_id=message_data.sender_id,
        content=message_data.content
    )
    db.add(group_message)
    db.commit()
    db.refresh(group_message)

    # Crear notificaciones para los otros miembros del grupo
    group_members = db.query(GroupMember).filter(GroupMember.group_id == group_id).all()
    for member in group_members:
        if member.user_id != message_data.sender_id:  # Excluir al remitente
            notification = Notification(
                user_id=member.user_id,
                message_id=group_message.id
            )
            db.add(notification)

    db.commit()
    return group_message

# Endpoint para obtener todos los mensajes de un grupo
@router.get("/{group_id}/messages", response_model=list[GroupMessageResponse])
def get_group_messages(group_id: int, db: Session = Depends(get_db)):
    messages = db.query(GroupMessage).filter(GroupMessage.group_id == group_id).order_by(GroupMessage.timestamp).all()
    return messages

# Endpoint para que un usuario abandone el grupo
@router.delete("/{group_id}/leave")
def leave_group(group_id: int, user_id: int, db: Session = Depends(get_db)):
    group_member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == user_id
    ).first()

    if not group_member:
        raise HTTPException(status_code=404, detail="User is not a member of the group")

    db.delete(group_member)
    db.commit()
    return {"message": "You have left the group"}
