from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app import models
from app.constants import BLOCK_LIMIT, BLOCK_DURATION_MINUTES


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, username: str):
    user = models.User(username=username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def increment_mentions(db: Session, user: models.User, count: int = 1):
    user.mention_count += count
    if user.mention_count > BLOCK_LIMIT:
        user.blocked = True
        user.blocked_at = datetime.utcnow()
    db.commit()


def unblock_expired(db: Session, user: models.User):
    if user.blocked and user.blocked_at:
        elapsed = datetime.utcnow() - user.blocked_at
        if elapsed > timedelta(minutes=BLOCK_DURATION_MINUTES):
            user.blocked = False
            user.mention_count = 0
            user.blocked_at = None
            db.commit()


def create_request(db: Session, user_id: int, content: str):
    req = models.Request(user_id=user_id, content=content)
    db.add(req)
    db.commit()
    db.refresh(req)
    return req


def save_result(db: Session, req_id: int, result: str):
    req = db.query(models.Request).filter(models.Request.id == req_id).first()
    req.result = result
    db.commit()


def unblock_user(db: Session, user: models.User):
    user.blocked = False
    user.mention_count = 0
    user.blocked_at = None
    db.commit()
