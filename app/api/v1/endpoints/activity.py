from fastapi import APIRouter, Depends, Request, Query
from app.schemas import CreateCategory, UpdateCategory
from app.db import db_depend
from app.crud import activity as activity_crud
from app.utils import admin_required


router = APIRouter(
	prefix = '/activities',
	tags=['Activity Log']
) 

@router.get("/activity-logs")
async def activity_logs_endpoint(
    db: db_depend,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
	admin = Depends(admin_required)
):
    return await activity_crud.get_activity_logs(db, page, limit)


@router.get("/activity-logs-by-entity")
async def activity_logs_endpoint(
    db: db_depend,
	entity: str,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
	admin = Depends(admin_required)
):
    return await activity_crud.get_activity_logs_by_entity(db, entity, page, limit)

@router.get("/activity-logs-by-user")
async def activity_logs_endpoint(
    db: db_depend,
	user_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
	admin = Depends(admin_required)
):
    return await activity_crud.get_activity_logs_by_user(db, user_id, page, limit)