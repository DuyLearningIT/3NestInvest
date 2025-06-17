from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import user as user_router
from app.api.v1.endpoints import category as cat_router
from app.api.v1.endpoints import type as type_router
from app.api.v1.endpoints import product as pro_router
from app.api.v1.endpoints import request as request_router
from app.api.v1.endpoints import order as order_router
# from app.api.v1.endpoints import chatbot as chatbot_router
from app.api.v1.endpoints import deal as deal_router
from app.api.v1.endpoints import permission_type as pm_type_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
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
# app.include_router(chatbot_router.router)
app.include_router(deal_router.router)
app.include_router(pm_type_router.router)


@app.get('/')
async def default():
	return {
		'mess' : 'API is running !',
        'status_code' : status.HTTP_200_OK
	}
