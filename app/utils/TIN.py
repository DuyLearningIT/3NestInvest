import httpx

async def get_info_from_tin(tin):
    with httpx.Client() as client:
        result = client.get(f'https://api.vietqr.io/v2/business/{tin}')
        return result.json()

