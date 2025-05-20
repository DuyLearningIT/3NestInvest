from fastapi import FastAPI
from app.api.v1.endpoints import user as user_router
from app.api.v1.endpoints import category as cat_router
from app.api.v1.endpoints import type as type_router
from app.api.v1.endpoints import product as pro_router
from app.utils import get_current_user

app = FastAPI()

app.include_router(user_router.router)
app.include_router(cat_router.router)
app.include_router(type_router.router)
app.include_router(pro_router.router)

@app.get('/')
async def default():
	return {
		'mess' : 'API is running !'
	}
