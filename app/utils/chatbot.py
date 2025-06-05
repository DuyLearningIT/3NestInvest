# from huggingface_hub import InferenceClient
# from fastapi import HTTPException, status

# hf_token = "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"

# client = InferenceClient(
#     model="meta-llama/Meta-Llama-3-8B-Instruct",
#     token=hf_token
# )

# async def chatbot(query: str):
#     try:
#         response = client.text_generation(
#             prompt=query,
#             max_new_tokens=256,
#             temperature=0.7,
#             do_sample=True,
#             return_full_text=False
#         )

#         return {
#             'mess': 'Ask chatbot successfully!',
#             'data': response,
#             'status_code': status.HTTP_200_OK
#         }

#     except Exception as ex:
#         raise HTTPException(
#             detail=f'Something went wrong: {ex}',
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )
