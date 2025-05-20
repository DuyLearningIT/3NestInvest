from sqlalchemy.orm import Session, load_only
from app.models import Type
from app.schemas import CRUDType, UpdateType
from datetime import datetime

def create_type(db: Session, request : CRUDType):
	check = db.query(Type).filter(Type.type_name == request.type_name).first()
	if check:
		return False
	new_type = Type(
		type_name = request.type_name,
		description = request.description
	)
	db.add(new_type)
	db.commit()
	db.refresh(new_type)

	return {
		'type_id' : new_type.type_id,
		'type_name' : new_type.type_name,
		'description' : new_type.description,
		'created_at' : new_type.created_at,
		'created_by' : new_type.created_by
	}

def get_types(db: Session):
	return db.query(Type).options(load_only(Type.type_id, Type.type_name, Type.description)).all()

def get_type(db : Session, type_id : int):
	check = db.query(Type).filter(Type.type_id == type_id).first()
	if check is None:
		return None
	return {
		'type_id' : check.type_id,
		'type_name' : check.type_name,
		'description' : check.description
	}

def update_type(db: Session, request: UpdateType):
	check = db.query(Type).filter(Type.type_id == request.type_id).first()
	if check is None:
		return None
	check.type_name = request.type_name or check.type_name
	check.description = request.description or check.description
	check.updated_at = datetime.now()
	check.updated_by = 'admin'

	db.commit()
	db.refresh(check)
	return {
		'type_id' : check.type_id,
		'type_name' : check.type_name,
		'description' : check.description,
		'updated_at': check.updated_at,
		'updated_by' : check.updated_by
	}

def delete_type(db: Session, type_id : int):
	check = db.query(Type).filter(Type.type_id == type_id).first()
	if check is None:
		return False
	db.delete(check)
	db.commit()
	return True