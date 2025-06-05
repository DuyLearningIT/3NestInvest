# from fastapi import APIRouter, Depends
# from app.utils import chatbot

# router = APIRouter(
# 	prefix = '/chatbot',
# 	tags=['Chatbot']
# )

# @router.get('/ask-chatbot')
# async def ask_chat_bot(query: str):
# 	response = await chatbot(query)
# 	return response