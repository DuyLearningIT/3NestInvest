from fastapi import APIRouter, Depends, Request, Query
from app.schemas import CreateCategory, UpdateCategory
from app.db import db_depend
from app.crud import activity as activity_crud
from app.utils import admin_required
from datetime import datetime
from typing import Optional


router = APIRouter(
	prefix = '/activities',
	tags=['Activity Log']
) 

# filter all 
@router.get("/activity-logs")
async def activity_logs(
    db: db_depend,
    user_email: Optional[str] = Query(None),
    entity: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    page: int = 1,
    limit: int = 50,
    admin = Depends(admin_required)
):
    return await activity_crud.get_activity_logs_filtered(
        db=db,
        user_email=user_email,
        entity=entity,
        start_date=start_date,
        end_date=end_date,
        page=page,
        limit=limit
    )