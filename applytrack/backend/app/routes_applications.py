from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from .database import get_db
from .dependencies import current_user
from .models import Application, User
from .schemas import ApplicationCreate, ApplicationRead, ApplicationUpdate, Statistics

router = APIRouter(prefix="/applications", tags=["applications"])
VALID_STATUSES = ("saved", "applied", "interview", "offer", "rejected")

@router.post("", response_model=ApplicationRead, status_code=201)
def create_application(payload: ApplicationCreate, db: Session = Depends(get_db), user: User = Depends(current_user)):
    item = Application(**payload.model_dump(mode="json"), owner_id=user.id)
    db.add(item); db.commit(); db.refresh(item)
    return item

@router.get("", response_model=list[ApplicationRead])
def list_applications(status_filter: str | None = Query(default=None, alias="status"), db: Session = Depends(get_db), user: User = Depends(current_user)):
    query = select(Application).where(Application.owner_id == user.id).order_by(Application.applied_at.desc())
    if status_filter:
        if status_filter not in VALID_STATUSES:
            raise HTTPException(422, "Unknown status")
        query = query.where(Application.status == status_filter)
    return list(db.scalars(query))

@router.get("/statistics", response_model=Statistics)
def statistics(db: Session = Depends(get_db), user: User = Depends(current_user)):
    rows = db.execute(select(Application.status, func.count()).where(Application.owner_id == user.id).group_by(Application.status)).all()
    counts = {key: 0 for key in VALID_STATUSES}
    counts.update({key: count for key, count in rows})
    total = sum(counts.values())
    contacted = counts["interview"] + counts["offer"]
    return Statistics(total=total, by_status=counts, response_rate=round(contacted / total, 4) if total else 0.0)

@router.get("/{application_id}", response_model=ApplicationRead)
def get_application(application_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    item = db.scalar(select(Application).where(Application.id == application_id, Application.owner_id == user.id))
    if not item: raise HTTPException(404, "Application not found")
    return item

@router.patch("/{application_id}", response_model=ApplicationRead)
def update_application(application_id: int, payload: ApplicationUpdate, db: Session = Depends(get_db), user: User = Depends(current_user)):
    item = db.scalar(select(Application).where(Application.id == application_id, Application.owner_id == user.id))
    if not item: raise HTTPException(404, "Application not found")
    for key, value in payload.model_dump(exclude_unset=True, mode="json").items():
        setattr(item, key, value)
    db.commit(); db.refresh(item)
    return item

@router.delete("/{application_id}", status_code=204)
def delete_application(application_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    item = db.scalar(select(Application).where(Application.id == application_id, Application.owner_id == user.id))
    if not item: raise HTTPException(404, "Application not found")
    db.delete(item); db.commit()
