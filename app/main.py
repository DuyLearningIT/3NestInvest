from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import user as user_router
from app.api.v1.endpoints import category as cat_router
from app.api.v1.endpoints import type as type_router
from app.api.v1.endpoints import product as pro_router
from app.api.v1.endpoints import request as request_router
from app.api.v1.endpoints import order as order_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*", 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)
app.include_router(cat_router.router)
app.include_router(type_router.router)
app.include_router(pro_router.router)
app.include_router(request_router.router)
app.include_router(order_router.router)

@app.get('/')
async def default():
	return {
		'mess' : 'API is running !'
	}
